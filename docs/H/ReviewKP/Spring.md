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