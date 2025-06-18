#Review knowledge points

这里会记录一些我在复习中觉得比较重要，或者我自己本身有点薄弱的点，方便后续回顾

## Java basic

GraalVM, 是一个JDK，提供了AOT编译和二进制打包的能力，打出来的二进制包可以实现快速启动、具有超高性能、无需预热时间、同时需要非常少的资源消耗
* 对于 JIT 而言，我们都知道Java类会被编译为 .class 格式的文件，这里编译后就是 jvm 识别的字节码，在 Java 应用运行的过程中，而 JIT 编译器又将一些热点路径上的字节码编译为机器码，已实现更快的执行速度；
* 对于 AOT 模式来说，它直接在编译期间就将字节码转换为机器码，直接省去了运行时对jvm的依赖，由于省去了 jvm 加载和字节码运行期预热的时间，AOT 编译和打包的程序具有非常高的运行时效率。

JIT 使得应用可以具备更高的极限处理能力，可以降低请求的最大延迟这一关键指标；而 AOT 则可以进一步的提升应用的冷启动速度、具有更小的二进制包提及、在运行态需要更少的内存等资源。

Native Image 是一项将 Java 代码编译打包为可执行二进制程序的技术，解决 Java 应用在 Sererless 等云计算应用场景中面临的启动慢，包占用空间大等突出问题。

但是GraalVM 无法识别代码中的一些动态调用行为，如反射、resource资源加载、序列化、动态代理等都动态行为都将受限


***

基本数据类型的**局部**变量存放在 Java **虚拟机栈中的局部变量表**中，也正是因为这样，基本数据类型在操作的时候会比较快。但是成员变量（未被static修饰）会存在堆中，被static修饰了的会存放在方法区中。

hotspot引入了JIT后，会对对象进行逃逸分析（如果这个局部变量没有被传递到其他的方法中，我们就认为这个局部变量没有逃逸），没有逃逸的会通过**标量替换**存到栈里，避免存放到堆内存。

| 包装类 | 缓存区间 |
|--------|----------|
| Byte | -128 ~ 127 |
| Short | -128 ~ 127 |
| Integer | -128 ~ 127 |
| Long | -128 ~ 127 |
| Character | 0 ~ 127 |
| Boolean | true/false |
| Float | 无缓存 |
| Double | 无缓存 |

注意：
1. 这些包装类在缓存区间内的值会直接从缓存中获取，而不是创建新对象
2. Float和Double没有缓存，因为浮点数的范围太大，缓存的意义不大
3. Character只缓存ASCII码范围内的字符（0-127）
4. Boolean只有两个值，所以全部缓存
5. -XX:AutoBoxCacheMax=<size> 可以修改Integer的缓存大小，但是只能修改正数。

Integer.valueOf会判断所传入的数值会不会在缓存中
new Interger 的话不会从缓存中取了


***

String类在JDK9后把char[]（2个字节，16位） 就改成了byte[]（1个字节，8位），这样在new String后会节省一半的空间，但是因为有字符集的问题，比如中文就会站占2个字符集，但是LAITN的话就只会占一个，所以在一些方法中，就会有针对与字符集的判断，已保证功能和原先一致

```java
  public int compareTo(String anotherString) {
        byte[] v1 = value;
        byte[] v2 = anotherString.value;
        byte coder = coder();
        if (coder == anotherString.coder()) {
            return coder == LATIN1 ? StringLatin1.compareTo(v1, v2)
                                   : StringUTF16.compareTo(v1, v2);
        }
        return coder == LATIN1 ? StringLatin1.compareToUTF16(v1, v2)
                               : StringUTF16.compareToLatin1(v1, v2);
     }
 ```

String类被设计为final的原因主要有以下几点：

1. **安全性**
   - 防止String类被继承和修改，避免子类破坏String的不可变性
   - 确保String对象的行为是可预测的，避免被恶意代码修改

2. **性能优化**
   - 允许JVM对String进行优化，如字符串常量池的实现
   - 由于String不可变，可以在多线程环境下安全地共享
   - 支持字符串常量池的缓存机制，提高性能

3. **设计理念**
   - String作为最基础的数据类型之一，需要保证其行为的稳定性和可靠性
   - 不可变性是String的核心特性，final修饰符可以强制实现这一特性

4. **缓存优化**
   - 由于String不可变，可以安全地缓存其hashCode值
   - 在String类中，hashCode被缓存为实例变量，避免重复计算

5. **安全性考虑**
   - 在Java中，String经常用于存储敏感信息（如密码）
   - 不可变性可以防止这些信息被意外修改

这些原因共同决定了String类需要被设计为final，以确保其安全性、可靠性和性能。


 ***


### hashCode和equals的区别

1. **equals方法**
   - 用于判断两个对象是否相等
   - 默认实现是比较对象的内存地址（==）
   - 通常需要根据业务逻辑重写，比如判断两个对象的属性值是否相等

2. **hashCode方法**
   - 返回对象的哈希码值
   - 用于哈希表（如HashMap、HashSet）中快速定位对象
   - 默认实现是基于对象的内存地址

### 为什么重写equals必须重写hashCode

1. **哈希表的一致性要求**
   - 如果两个对象通过equals比较相等，那么它们的hashCode必须相等
   - 如果两个对象的hashCode相等，它们不一定通过equals比较相等（哈希冲突）

2. **违反规则的问题**
   - 如果只重写equals而不重写hashCode，会导致在哈希表中出现不一致
   - 例如：两个对象通过equals比较相等，但hashCode不同，在HashMap中会被当作不同的对象存储




***
以下是@Transactional注解失效的常见场景及原因：

1. **方法访问权限问题**
   - 非public方法上的@Transactional注解会失效
   - Spring默认只对public方法进行事务代理
   ```java
   @Service
   public class UserService {
       @Transactional
       private void updateUser() {  // 事务失效
           // 更新用户信息
       }
   }
   ```

2. **方法调用方式问题**
   - 同一个类中的方法直接调用，事务会失效
   - 因为Spring的事务管理是通过AOP代理实现的，内部方法调用不会经过代理
   ```java
   @Service
   public class OrderService {
       public void createOrder() {
           this.updateOrder();  // 事务失效
       }
       
       @Transactional
       public void updateOrder() {
           // 更新订单
       }
   }
   ```

3. **异常处理问题**
   - 异常被捕获但未抛出，事务会失效
   - 抛出的异常类型不在rollbackFor指定的范围内
   ```java
   @Service
   public class PaymentService {
       @Transactional
       public void processPayment() {
           try {
               // 处理支付
               throw new RuntimeException("支付失败");
           } catch (Exception e) {
               // 捕获异常但未抛出，事务失效
               log.error("支付异常", e);
           }
       }
   }
   ```

4. **数据库引擎不支持**
   - 使用MyISAM等不支持事务的数据库引擎
   - 事务注解将不会生效
   ```sql
   CREATE TABLE users (
       id INT PRIMARY KEY,
       name VARCHAR(100)
   ) ENGINE=MyISAM;  -- 不支持事务
   ```

5. **Bean未被Spring管理**
   - 类未被@Component、@Service等注解标记
   - 或未被正确扫描到Spring容器中
   ```java
   // 缺少@Service注解，事务失效
   public class ProductService {
       @Transactional
       public void updateProduct() {
           // 更新产品
       }
   }
   ```

6. **事务传播行为设置不当**
   - 如果方法的事务传播行为设置为NOT_SUPPORTED、NEVER等
   - 会导致事务不生效
   ```java
   @Service
   public class InventoryService {
       @Transactional(propagation = Propagation.NOT_SUPPORTED)
       public void updateStock() {  // 事务失效
           // 更新库存
       }
   }
   ```

7. **配置问题**
   - 未开启事务管理（@EnableTransactionManagement）
   - 事务管理器配置错误
   ```java
   @Configuration
   public class AppConfig {
       // 缺少@EnableTransactionManagement注解
       // 或事务管理器配置错误
       @Bean
       public PlatformTransactionManager transactionManager() {
           return new DataSourceTransactionManager(dataSource());
       }
   }
   ```


***

关于[线程池的介绍](https://mp.weixin.qq.com/s/ndBdf7InQPZq40uoqBUTSw)

```java
public ThreadPoolExecutor(int corePoolSize,
                              int maximumPoolSize,
                              long keepAliveTime,
                              TimeUnit unit,
                              BlockingQueue<Runnable> workQueue,
                              ThreadFactory threadFactory,
                              RejectedExecutionHandler handler) {
        if (corePoolSize < 0 ||
            maximumPoolSize <= 0 ||
            maximumPoolSize < corePoolSize ||
            keepAliveTime < 0)
            throw new IllegalArgumentException();
        if (workQueue == null || threadFactory == null || handler == null)
            throw new NullPointerException();
        this.corePoolSize = corePoolSize;
        this.maximumPoolSize = maximumPoolSize;
        this.workQueue = workQueue;
        this.keepAliveTime = unit.toNanos(keepAliveTime);
        this.threadFactory = threadFactory;
        this.handler = handler;

        String name = Objects.toIdentityString(this);
        this.container = SharedThreadContainer.create(name);
    }
```    

* corePoolSize：线程池中用来工作的核心的线程数量。
* maximumPoolSize：最大线程数，线程池允许创建的最大线程数。
* keepAliveTime：超出 corePoolSize 后创建的线程存活时间或者是所有线程最大存活时间，取决于配置。
* unit：keepAliveTime 的时间单位。
* workQueue：任务队列，是一个阻塞队列，当线程数已达到核心线程数，会将任务存储在阻塞队列中。
* threadFactory ：线程池内部创建线程所用的工厂。
* handler：拒绝策略；当队列已满并且线程数量达到最大线程数量时，会调用该方法处理该任务。


RejectedExecutionHandler的实现JDK自带的默认有4种
* AbortPolicy：丢弃任务，抛出运行时异常
* CallerRunsPolicy：由提交任务的线程来执行任务
* DiscardPolicy：丢弃这个任务，但是不抛异常
* DiscardOldestPolicy：从队列中剔除最先进入队列的任务，然后再次提交任务


任务队列

* LinkedBlockingQueue：无界队列（默认 Integer.MAX_VALUE），易堆积任务导致 OOM。
* ArrayBlockingQueue：有界队列，需指定容量（如 new ArrayBlockingQueue<>(100)）。
* SynchronousQueue：不存储任务，直接移交线程执行，适合高吞吐但拒绝策略需谨慎。

在工作中创建线程池可以选择ArrayBolckingQueue和CallerRunsPolicy的搭配，保证任务不丢失。

​IO 密集型​：核心线程数建议 2N + 1（N 为 CPU 核数）。

​CPU 密集型​：核心线程数设为 N + 1。

***

当禁止多表join的时候，该如何处理？
1. 在应用层对数据进行拼接
2. 反范式设计，创建冗余表
3. ETL + 宽表，通过离线任务ETL来生成数据，适合T+1
4. 分布式优化数据库
    1. 小表驱动大表
    2. 关联字段必须加索引
    3. 控制查询字段
    4. 调整数据库配置：增大 join_buffer_size 提升 Block Nested-Loop 性能；




 ***

OSI七层协议从下到上依次是：

1. 物理层（Physical Layer）
   - 负责在物理媒介上传输原始比特流
   - 定义电气、机械、功能和规程特性
   - 主要设备：中继器、集线器

2. 数据链路层（Data Link Layer）
   - 将比特流组装成帧
   - 提供物理寻址、错误检测和流量控制
   - 主要设备：网桥、交换机
   - 协议：PPP、HDLC

3. 网络层（Network Layer）
   - 负责数据包的路由选择
   - 提供逻辑寻址
   - 主要设备：路由器
   - 协议：IP、ICMP、IGMP

4. 传输层（Transport Layer）
   - 提供端到端的可靠数据传输
   - 负责流量控制和错误恢复
   - 协议：TCP、UDP

5. 会话层（Session Layer）
   - 建立、管理和终止会话
   - 提供会话控制
   - 协议：RPC、SQL

6. 表示层（Presentation Layer）
   - 数据格式转换
   - 数据加密解密
   - 数据压缩解压缩
   - 协议：JPEG、ASCII

7. 应用层（Application Layer）
   - 为用户提供网络服务
   - 提供应用程序接口
   - 协议：HTTP、FTP、SMTP、DNS

记忆口诀：物数网传会表应（物理层、数据链路层、网络层、传输层、会话层、表示层、应用层）