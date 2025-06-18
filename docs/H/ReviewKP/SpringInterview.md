# Spring Boot & Spring Cloud 深度面试题

## Spring Boot 核心问题

### 1. Spring Boot 的自动配置原理是什么？

**答案：**
Spring Boot 的自动配置主要通过 `@EnableAutoConfiguration` 注解实现，其核心原理如下：

1. **启动流程**：
   - Spring Boot 启动时，会加载 `META-INF/spring.factories` 文件
   - 该文件中定义了大量的自动配置类（AutoConfiguration）
   - 这些配置类都使用 `@Conditional` 注解进行条件判断

2. **条件注解机制**：
```java
@Configuration
@ConditionalOnClass({DataSource.class, EmbeddedDatabaseType.class})
@ConditionalOnProperty(prefix = "spring.datasource", name = "url")
public class DataSourceAutoConfiguration {
    // 配置内容
}
```

3. **配置优先级**：
   - 用户配置 > 自动配置 > 默认配置
   - 通过 `@SpringBootApplication(exclude = {DataSourceAutoConfiguration.class})` 可以排除特定自动配置

### 2. Spring Boot 中的事务传播机制和隔离级别

**答案：**

1. **传播机制（Propagation）**：
```java
@Service
public class UserService {
    @Transactional(propagation = Propagation.REQUIRED)
    public void method1() {
        // 如果当前没有事务，就创建一个新事务
    }
    
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void method2() {
        // 总是创建一个新事务
    }
    
    @Transactional(propagation = Propagation.NESTED)
    public void method3() {
        // 如果当前存在事务，则创建一个嵌套事务
    }
}
```

2. **隔离级别（Isolation）**：
```java
@Transactional(isolation = Isolation.READ_COMMITTED)
public void method() {
    // 读已提交，解决脏读
}

@Transactional(isolation = Isolation.REPEATABLE_READ)
public void method() {
    // 可重复读，解决不可重复读
}

@Transactional(isolation = Isolation.SERIALIZABLE)
public void method() {
    // 串行化，解决幻读
}
```

### 3. Spring Boot 中的缓存机制

**答案：**

1. **缓存注解使用**：
```java
@Service
public class UserService {
    @Cacheable(value = "users", key = "#id")
    public User findById(Long id) {
        return userRepository.findById(id);
    }
    
    @CachePut(value = "users", key = "#user.id")
    public User updateUser(User user) {
        return userRepository.save(user);
    }
    
    @CacheEvict(value = "users", key = "#id")
    public void deleteUser(Long id) {
        userRepository.deleteById(id);
    }
}
```

2. **缓存配置**：
```java
@Configuration
@EnableCaching
public class CacheConfig {
    @Bean
    public CacheManager cacheManager() {
        CaffeineCacheManager cacheManager = new CaffeineCacheManager();
        cacheManager.setCaffeine(Caffeine.newBuilder()
            .expireAfterWrite(60, TimeUnit.MINUTES)
            .maximumSize(100));
        return cacheManager;
    }
}
```

## Spring Cloud 核心问题

### 1. 服务注册与发现（Eureka）的工作原理

**答案：**

1. **服务注册流程**：
```java
@SpringBootApplication
@EnableEurekaClient
public class ServiceApplication {
    public static void main(String[] args) {
        SpringApplication.run(ServiceApplication.class, args);
    }
}
```

2. **服务发现机制**：
```java
@Service
public class UserService {
    @Autowired
    private DiscoveryClient discoveryClient;
    
    public List<ServiceInstance> getServiceInstances(String serviceId) {
        return discoveryClient.getInstances(serviceId);
    }
}
```

3. **自我保护机制**：
   - 当Eureka Server节点在短时间内丢失过多客户端时，会进入自我保护模式
   - 配置示例：
```yaml
eureka:
  server:
    enable-self-preservation: true
    renewal-percent-threshold: 0.85
```

### 2. 负载均衡（Ribbon）的实现原理

**答案：**

1. **自定义负载均衡策略**：
```java
@Configuration
public class RibbonConfig {
    @Bean
    public IRule ribbonRule() {
        return new WeightedResponseTimeRule();
    }
}
```

2. **重试机制**：
```yaml
ribbon:
  ConnectTimeout: 1000
  ReadTimeout: 3000
  MaxAutoRetries: 1
  MaxAutoRetriesNextServer: 2
  OkToRetryOnAllOperations: true
```

### 3. 熔断器（Hystrix）的使用和原理

**答案：**

1. **基本使用**：
```java
@Service
public class UserService {
    @HystrixCommand(fallbackMethod = "getUserFallback")
    public User getUser(Long id) {
        return userClient.getUser(id);
    }
    
    public User getUserFallback(Long id) {
        return new User(id, "fallback");
    }
}
```

2. **熔断器配置**：
```java
@Configuration
public class HystrixConfig {
    @Bean
    public HystrixCommandProperties.Setter hystrixCommandProperties() {
        return HystrixCommandProperties.Setter()
            .withCircuitBreakerEnabled(true)
            .withCircuitBreakerRequestVolumeThreshold(20)
            .withCircuitBreakerErrorThresholdPercentage(50)
            .withCircuitBreakerSleepWindowInMilliseconds(5000);
    }
}
```

### 4. 配置中心（Config）的使用

**答案：**

1. **服务端配置**：
```java
@SpringBootApplication
@EnableConfigServer
public class ConfigServerApplication {
    public static void main(String[] args) {
        SpringApplication.run(ConfigServerApplication.class, args);
    }
}
```

2. **客户端配置**：
```yaml
spring:
  cloud:
    config:
      uri: http://localhost:8888
      fail-fast: true
      retry:
        initial-interval: 1000
        max-attempts: 6
        max-interval: 2000
        multiplier: 1.1
```

### 5. 网关（Gateway）的使用和原理

**答案：**

1. **路由配置**：
```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: user-service
          uri: lb://user-service
          predicates:
            - Path=/user/**
          filters:
            - StripPrefix=1
            - AddRequestHeader=X-Request-From, Gateway
```

2. **自定义过滤器**：
```java
@Component
public class AuthFilter implements GlobalFilter {
    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        ServerHttpRequest request = exchange.getRequest();
        // 实现认证逻辑
        return chain.filter(exchange);
    }
}
```

## 高级特性

### 1. Spring Boot 中的异步处理

**答案：**

1. **异步方法**：
```java
@Service
public class AsyncService {
    @Async
    public CompletableFuture<String> asyncMethod() {
        return CompletableFuture.supplyAsync(() -> {
            // 异步处理逻辑
            return "result";
        });
    }
}
```

2. **线程池配置**：
```java
@Configuration
@EnableAsync
public class AsyncConfig implements AsyncConfigurer {
    @Override
    public Executor getAsyncExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(10);
        executor.setMaxPoolSize(20);
        executor.setQueueCapacity(500);
        executor.setThreadNamePrefix("Async-");
        executor.initialize();
        return executor;
    }
}
```

### 2. Spring Cloud 中的分布式事务

**答案：**

1. **Seata 配置**：
```java
@Configuration
public class SeataConfig {
    @Bean
    public GlobalTransactionScanner globalTransactionScanner() {
        return new GlobalTransactionScanner("user-service", "my_test_tx_group");
    }
}
```

2. **事务使用**：
```java
@Service
public class OrderService {
    @GlobalTransactional
    public void createOrder(Order order) {
        orderMapper.insert(order);
        accountService.decrease(order.getUserId(), order.getAmount());
        storageService.decrease(order.getProductId(), order.getCount());
    }
}
```

## 性能优化

### 1. Spring Boot 应用性能优化

**答案：**

1. **JVM 调优**：
```bash
java -Xms2g -Xmx2g -XX:+UseG1GC -jar application.jar
```

2. **连接池配置**：
```yaml
spring:
  datasource:
    hikari:
      maximum-pool-size: 10
      minimum-idle: 5
      idle-timeout: 300000
      connection-timeout: 20000
      max-lifetime: 1200000
```

### 2. Spring Cloud 微服务性能优化

**答案：**

1. **服务调用优化**：
```yaml
feign:
  hystrix:
    enabled: true
  client:
    config:
      default:
        connectTimeout: 5000
        readTimeout: 5000
```

2. **缓存优化**：
```java
@Configuration
@EnableCaching
public class CacheConfig {
    @Bean
    public CacheManager cacheManager() {
        RedisCacheManager.RedisCacheManagerBuilder builder = RedisCacheManager
            .RedisCacheManagerBuilder
            .fromConnectionFactory(redisConnectionFactory());
        return builder
            .cacheDefaults(defaultConfig())
            .withCacheConfiguration("users", userConfig())
            .build();
    }
}
``` 