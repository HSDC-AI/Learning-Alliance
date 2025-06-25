# Spring

当我们没有使用spring boot，而使用Spring的时候，这段代码就能直接的将我们的spring 工程给启动起来，就是@SpringBootApplication 这个注解的老版。
```java
ApplicationContext context = new ClassPathXmlApplicationContext("classpath:applicationfile.xml");
```
![applicationContext 及子类的关系](applicationContextLevel.png)


## Bean 的生命周期
1. 创建Bean实例：Bean容器首先会找到Bean的定义，然后使用Java反射API来创建Bean的实例
2. Bean的属性赋值填充：为 Bean 设置相关属性和依赖，例如@Autowired 等注解注入的对象、@Value 注入的值、setter方法或构造函数注入依赖和值、@Resource注入的各种资源。
3. Bean的初始化
    1. 如果 Bean 实现了 BeanNameAware 接口，调用 setBeanName()方法，传入 Bean 的名字。
    2. 如果 Bean 实现了 BeanClassLoaderAware 接口，调用 setBeanClassLoader()方法，传入 ClassLoader对象的实例。
    3. 如果 Bean 实现了 BeanFactoryAware 接口，调用 setBeanFactory()方法，传入 BeanFactory对象的实例。
    4. 上面的类似，如果实现了其他 *.Aware接口，就调用相应的方法。
    5. 如果有和加载这个 Bean 的 Spring 容器相关的 BeanPostProcessor 对象，执行postProcessBeforeInitialization() 方法
    6. 如果 Bean 实现了InitializingBean接口，执行afterPropertiesSet()方法
    7. 如果 Bean 在配置文件中的定义包含 init-method 属性，执行指定的方法
    8. 如果有和加载这个 Bean 的 Spring 容器相关的 BeanPostProcessor 对象，执行postProcessAfterInitialization() 方法。
4. 销毁并不是说要立马把 Bean 给销毁掉，而是把 Bean 的销毁方法先记录下来，将来需要销毁 Bean 或者销毁容器的时候，就调用这些方法去释放 Bean 所持有的资源。
    1. 如果 Bean 实现了 DisposableBean 接口，执行 destroy() 方法
    2. 如果 Bean 在配置文件中的定义包含 destroy-method 属性，执行指定的 Bean 销毁方法。或者，也可以直接通过@PreDestroy 注解标记 Bean 销毁之前执行的方法。    


## Spring Boot 应用生命周期

Spring Boot 应用的生命周期比传统的 Spring 应用更加复杂，包含了应用启动、运行和关闭的完整过程。

### 1. 应用启动阶段

#### 1.1 环境准备
- **Bootstrap 阶段**：Spring Boot 2.4+ 引入了 bootstrap 上下文
- **环境变量加载**：加载系统环境变量、JVM 参数
- **配置文件加载**：按优先级加载 application.properties/application.yml 等配置文件

#### 1.2 自动配置阶段
```java
@SpringBootApplication
public class MyApplication {
    public static void main(String[] args) {
        SpringApplication.run(MyApplication.class, args);
    }
}
```

**自动配置过程**：
1. **@EnableAutoConfiguration**：启用自动配置
2. **@ComponentScan**：扫描组件
3. **@Configuration**：配置类处理
4. **条件注解评估**：@ConditionalOnClass、@ConditionalOnProperty 等
5. **Bean 定义注册**：将符合条件的 Bean 定义注册到容器

#### 1.3 应用上下文创建
- **ApplicationContext 创建**：根据应用类型创建相应的 ApplicationContext
- **Bean 工厂准备**：准备 BeanFactory 和相关的后处理器
- **环境配置**：设置应用环境（dev、test、prod 等）

### 2. 应用运行阶段

#### 2.1 事件监听机制
Spring Boot 提供了丰富的事件监听机制：

```java
@Component
public class ApplicationEventListener {
    
    @EventListener
    public void handleApplicationReady(ApplicationReadyEvent event) {
        // 应用启动完成后的处理
    }
    
    @EventListener
    public void handleApplicationStarted(ApplicationStartedEvent event) {
        // 应用启动事件处理
    }
}
```

#### 2.2 生命周期事件顺序
1. **ApplicationStartingEvent**：应用启动时触发
2. **ApplicationEnvironmentPreparedEvent**：环境准备完成
3. **ApplicationContextInitializedEvent**：应用上下文初始化
4. **ApplicationPreparedEvent**：应用准备完成
5. **ApplicationStartedEvent**：应用启动
6. **ApplicationReadyEvent**：应用就绪
7. **ApplicationFailedEvent**：应用启动失败

### 3. 应用关闭阶段

#### 3.1 优雅关闭
```java
@Component
public class GracefulShutdown {
    
    @PreDestroy
    public void onShutdown() {
        // 应用关闭前的清理工作
    }
}
```

#### 3.2 关闭流程
1. **接收关闭信号**：SIGTERM、SIGINT 等信号
2. **停止接收新请求**：Web 服务器停止接收新连接
3. **等待现有请求完成**：等待正在处理的请求完成
4. **Bean 销毁**：按照依赖关系逆序销毁 Bean
5. **资源释放**：释放数据库连接、线程池等资源
6. **应用退出**：JVM 退出

### 4. 关键接口和注解

#### 4.1 生命周期接口
```java
// 应用启动器
public interface ApplicationRunner {
    void run(ApplicationArguments args) throws Exception;
}

// 命令行运行器
public interface CommandLineRunner {
    void run(String... args) throws Exception;
}
```

#### 4.2 生命周期注解
- **@PostConstruct**：Bean 初始化后执行
- **@PreDestroy**：Bean 销毁前执行
- **@EventListener**：事件监听
- **@Order**：执行顺序控制

### 5. 配置和监控

#### 5.1 健康检查
```java
@Component
public class CustomHealthIndicator implements HealthIndicator {
    @Override
    public Health health() {
        // 自定义健康检查逻辑
        return Health.up().build();
    }
}
```

#### 5.2 应用信息
```properties
# application.properties
management.endpoints.web.exposure.include=health,info,metrics
management.endpoint.health.show-details=always
```

### 6. 最佳实践

1. **启动优化**：使用懒加载、条件配置减少启动时间
2. **优雅关闭**：实现 PreDestroy 方法进行资源清理
3. **健康检查**：提供应用健康状态监控
4. **日志记录**：记录关键生命周期事件
5. **错误处理**：妥善处理启动失败和运行时异常


