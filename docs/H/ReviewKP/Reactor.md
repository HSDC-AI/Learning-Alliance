# Java Reactor 指南

## 什么是 Project Reactor？
Project Reactor 是一个用于在 JVM 上构建非阻塞应用程序的第四代响应式库。它是 Spring 生态系统中响应式技术栈（如 Spring WebFlux）的基础。Reactor 实现了 Reactive Streams 规范，提供了一种强大而富有表现力的方式来处理异步数据流。

## 核心概念：`Flux` 和 `Mono`
Reactor 提供了两种核心的发布者（Publisher）类型，它们是数据流的源头：

- **`Flux<T>`**: 表示一个包含 0 到 N 个元素的异步序列。它可以是一个有限的数据流，也可以是一个无限的数据流（例如，来自消息队列的事件）。
- **`Mono<T>`**: 表示一个包含 0 或 1 个元素的异步结果。它非常适合表示那些可能异步完成并且只返回一个结果的操作（例如，HTTP 请求的响应）。

## 创建 `Flux` 和 `Mono`
创建响应式流有多种方式，以下是一些常见的工厂方法：

```java
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import java.util.Arrays;
import java.util.List;

// 从静态数据创建 Flux
Flux<String> fluxFromJust = Flux.just("Apple", "Banana", "Cherry");

// 从集合创建 Flux
List<String> fruits = Arrays.asList("Orange", "Grape", "Strawberry");
Flux<String> fluxFromIterable = Flux.fromIterable(fruits);

// 创建一个整数范围的 Flux
Flux<Integer> fluxFromRange = Flux.range(1, 5); // 包含 1, 2, 3, 4, 5

// 创建一个包含单个值的 Mono
Mono<String> monoFromJust = Mono.just("OneValue");

// 创建一个可能为空的 Mono
Mono<String> monoFromNullable = Mono.justOrEmpty(null); // 返回一个空的 Mono
Mono<String> nonEmptyMono = Mono.justOrEmpty("Value"); // 返回一个包含值的 Mono

// 订阅并触发数据流
fluxFromJust.subscribe(fruit -> System.out.println("Consumed: " + fruit));
```

## 常用操作符
操作符是 Reactor 的核心。它们允许你以声明式的方式对数据流进行转换、过滤、组合和处理。

### 转换操作符 (`map`, `flatMap`)
- **`map`**: 同步地将一个元素转换为另一个元素。
- **`flatMap`**: 异步地将一个元素转换为一个新的流 (`Mono` 或 `Flux`)，然后将这些新流“扁平化”合并成一个单一的流。这是执行异步操作（如调用外部 API）的关键。

```java
// map: 将水果名称转换为大写
Flux.just("apple", "banana")
    .map(String::toUpperCase)
    .subscribe(System.out::println); // 输出 APPLE, BANANA

// flatMap: 模拟异步获取用户订单
Flux.just("user-1", "user-2")
    .flatMap(userId -> fetchOrdersForUser(userId)) // fetchOrdersForUser 返回一个 Flux<String>
    .subscribe(order -> System.out.println("Received " + order));

// 模拟的异步服务调用
public Flux<String> fetchOrdersForUser(String userId) {
    // 在真实应用中，这里会是一个数据库查询或 HTTP 请求
    return Flux.defer(() -> Flux.just(userId + "'s Order 1", userId + "'s Order 2"))
               .delayElements(Duration.ofMillis(100)); // 模拟网络延迟
}
```

### 过滤操作符 (`filter`)
只允许满足条件的元素通过。

```java
Flux.range(1, 10)
    .filter(i -> i % 2 == 0) // 只保留偶数
    .subscribe(System.out::println); // 输出 2, 4, 6, 8, 10
```

### 组合操作符 (`zip`)
将多个流按照顺序组合在一起。当所有源流都发出一个元素时，`zip` 会将这些元素组合成一个元组，然后传递给下游。

```java
Flux<String> flux1 = Flux.just("A", "B", "C");
Flux<Integer> flux2 = Flux.just(1, 2, 3);

Flux.zip(flux1, flux2, (letter, number) -> letter + number)
    .subscribe(System.out::println); // 输出 A1, B2, C3
```

## 错误处理
响应式流中的错误是“一等公民”。你可以以声明式的方式处理它们。

```java
Flux.just(10, 5, 0, 2)
    .map(i -> 100 / i)
    .onErrorReturn("Error: Division by zero!") // 当发生错误时，返回一个默认值
    .subscribe(System.out::println);

Flux.<Integer>error(new RuntimeException("Something went wrong"))
    .onErrorResume(e -> {
        System.err.println("Caught error: " + e.getMessage());
        return Mono.just(-1); // 从错误中恢复，并提供一个备用值
    })
    .subscribe(System.out::println);
```

## 线程和调度器 (`Schedulers`)
Reactor 允许你精确控制代码在哪个线程上执行。

- **`subscribeOn(Scheduler)`**: 指定整个订阅链（从源头开始）在哪个线程池上执行。它只影响订阅发生的线程，并且通常只在链的开始处使用一次。
- **`publishOn(Scheduler)`**: 切换后续操作符在哪个线程池上执行。它只影响其后面的操作符。

```java
import reactor.core.scheduler.Schedulers;

Flux.range(1, 5)
    .map(i -> {
        System.out.println("Map running on thread: " + Thread.currentThread().getName());
        return i * 10;
    })
    .subscribeOn(Schedulers.boundedElastic()) // 指定数据源在有界弹性的线程池上发出数据
    .publishOn(Schedulers.parallel()) // 切换到并行的线程池来执行后续操作
    .filter(i -> {
        System.out.println("Filter running on thread: " + Thread.currentThread().getName());
        return i > 20;
    })
    .subscribe(i -> System.out.println("Received: " + i + " on thread: " + Thread.currentThread().getName()));
```

## 背压（Backpressure）
在响应式编程中，背压是一个至关重要的机制。它指的是当生产者（Publisher）发出数据的速度快于消费者（Subscriber）处理数据的速度时，消费者可以向生产者反向施加压力，请求生产者减慢发送速度或按需发送数据，从而防止消费者因数据积压而过载（例如，导致内存溢出）。

Reactor 遵循 Reactive Streams 规范，该规范内置了背压处理。这是通过 `Subscriber` 的 `request(n)` 方法实现的，它告诉上游的 `Publisher` 最多可以发送 `n` 个元素。

### 背压的代码示例
默认情况下，像 `subscribe(System.out::println)` 这样的简单订阅会隐式地请求无限数量的数据 (`Long.MAX_VALUE`)。为了手动控制背压，我们可以实现一个自定义的 `Subscriber`。

下面的例子展示了一个快速的发布者和一个处理速度很慢的订阅者。订阅者每次只向上游请求少量数据，从而控制数据流。

```java
import org.reactivestreams.Subscription;
import reactor.core.publisher.BaseSubscriber;
import reactor.core.publisher.Flux;

public class BackpressureExample {
    public static void main(String[] args) {
        Flux.range(1, 100) // 一个快速的发布者，会发出 100 个数字
            .doOnRequest(r -> System.out.println("Request of " + r))
            .subscribe(new BaseSubscriber<Integer>() {
                private int count = 0;
                private final int requestCount = 5; // 每次请求 5 个

                @Override
                protected void hookOnSubscribe(Subscription subscription) {
                    System.out.println("Subscribed! Requesting initial " + requestCount + " items.");
                    request(requestCount); // 首次订阅时，请求 5 个元素
                }

                @Override
                protected void hookOnNext(Integer value) {
                    count++;
                    System.out.println("Processing value: " + value);
                    // 模拟耗时的处理
                    try {
                        Thread.sleep(100);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }

                    if (count % requestCount == 0) {
                        System.out.println("Processed " + requestCount + " items. Requesting next batch...");
                        request(requestCount); // 每处理完一批，再请求下一批
                    }
                }

                @Override
                protected void hookOnComplete() {
                    System.out.println("Stream completed.");
                }

                @Override
                protected void hookOnError(Throwable throwable) {
                    System.err.println("Error: " + throwable.getMessage());
                }
            });
    }
}
```

#### 输出分析:
1. 程序启动后，`hookOnSubscribe` 被调用，它会打印 "Requesting initial 5 items." 并向上游请求 5 个元素。
2. 上游的 `Flux` 收到请求后，会发出 5 个数字。
3. 每处理一个数字，`hookOnNext` 都会打印 "Processing value: ..." 并暂停 100 毫秒。
4. 当处理完 5 个元素后 (`count % 5 == 0`)，它会再次调用 `request(5)`，请求下一批 5 个元素。
5. 这个过程会一直重复，直到所有 100 个数字都被处理完毕。

这个例子清晰地展示了消费者如何通过 `request()` 方法精确地控制数据流的速度，防止被快速的生产者压垮。

## Reactor 的实际用例

Project Reactor 因其非阻塞和事件驱动的特性，在以下场景中表现出色：

1.  **高性能 Web 后端 (Spring WebFlux)**
    - **场景**: 构建需要处理大量并发连接的微服务和 API，如实时仪表盘、聊天应用或物联网数据网关。
    - **优势**: WebFlux 使用 Reactor 和 Netty，可以用少量的线程处理极高的并发请求，从而减少内存消耗和上下文切换开销，提高系统的吞吐量和伸缩性。

2.  **数据流处理与集成**
    - **场景**: 从消息队列（如 Kafka, RabbitMQ）消费数据流，进行实时转换、过滤、聚合，然后再推送到另一个系统或数据库。
    - **优势**: Reactor 内置了背压（Backpressure）支持，可以自动处理消费者消费速度慢于生产者生产速度的情况，防止内存溢出。

3.  **服务编排与聚合**
    - **场景**: 一个前端请求需要后端从多个下游微服务（如用户服务、产品服务、库存服务）获取数据，然后聚合成一个单一的响应。
    - **优势**: 使用 `Mono.zip` 或 `Flux.flatMap` 可以并发地调用所有下游服务，而不是按顺序串行调用，从而显著缩短总响应时间。

4.  **响应式数据库访问 (R2DBC)**
    - **场景**: 构建一个完全非阻塞的数据访问层，以避免传统 JDBC 驱动的线程阻塞问题。
    - **优势**: R2DBC（Reactive Relational Database Connectivity）与 Reactor 结合使用，可以实现从 Web 层到数据库层的端到端响应式编程，最大化资源利用率。

5.  **实时通知和推送**
    - **场景**: 向客户端推送实时更新，如股票行情、体育比赛得分或系统状态更新。
    - **优势**: 可以使用 `Flux` 来表示一个无限的事件流，并利用 Server-Sent Events (SSE) 或 WebSocket 将其高效地推送到 Web 或移动客户端。 