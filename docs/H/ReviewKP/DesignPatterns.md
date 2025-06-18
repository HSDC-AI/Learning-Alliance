# 设计模式总结

设计模式是软件开发中常见问题的解决方案，它们可以帮助我们写出更好的代码。以下是23种设计模式的总结和示例代码。

## 创建型模式（5种）

### 1. 单例模式（Singleton Pattern）
确保一个类只有一个实例，并提供一个全局访问点。

```java
public class Singleton {
    private static volatile Singleton instance;
    
    private Singleton() {}
    
    public static Singleton getInstance() {
        if (instance == null) {
            synchronized (Singleton.class) {
                if (instance == null) {
                    instance = new Singleton();
                }
            }
        }
        return instance;
    }
}
```

### 2. 工厂方法模式（Factory Method Pattern）
定义一个创建对象的接口，让子类决定实例化哪个类。

```java
public interface Product {
    void operation();
}

public class ConcreteProduct implements Product {
    @Override
    public void operation() {
        System.out.println("ConcreteProduct operation");
    }
}

public abstract class Creator {
    public abstract Product factoryMethod();
}

public class ConcreteCreator extends Creator {
    @Override
    public Product factoryMethod() {
        return new ConcreteProduct();
    }
}
```

### 3. 抽象工厂模式（Abstract Factory Pattern）
提供一个创建一系列相关或相互依赖对象的接口，而无需指定它们具体的类。

```java
public interface AbstractFactory {
    ProductA createProductA();
    ProductB createProductB();
}

public class ConcreteFactory1 implements AbstractFactory {
    @Override
    public ProductA createProductA() {
        return new ConcreteProductA1();
    }
    
    @Override
    public ProductB createProductB() {
        return new ConcreteProductB1();
    }
}
```

### 4. 建造者模式（Builder Pattern）
将一个复杂对象的构建与它的表示分离，使同样的构建过程可以创建不同的表示。

```java
public class Computer {
    private String cpu;
    private String ram;
    private String storage;
    
    public static class Builder {
        private Computer computer = new Computer();
        
        public Builder cpu(String cpu) {
            computer.cpu = cpu;
            return this;
        }
        
        public Builder ram(String ram) {
            computer.ram = ram;
            return this;
        }
        
        public Builder storage(String storage) {
            computer.storage = storage;
            return this;
        }
        
        public Computer build() {
            return computer;
        }
    }
}
```

### 5. 原型模式（Prototype Pattern）
用原型实例指定创建对象的种类，并通过拷贝这些原型创建新的对象。

```java
public class Prototype implements Cloneable {
    @Override
    protected Object clone() throws CloneNotSupportedException {
        return super.clone();
    }
}
```

## 结构型模式（7种）

### 6. 适配器模式（Adapter Pattern）
将一个类的接口转换成客户希望的另外一个接口。

```java
public interface Target {
    void request();
}

public class Adaptee {
    public void specificRequest() {
        System.out.println("Adaptee specific request");
    }
}

public class Adapter implements Target {
    private Adaptee adaptee;
    
    public Adapter(Adaptee adaptee) {
        this.adaptee = adaptee;
    }
    
    @Override
    public void request() {
        adaptee.specificRequest();
    }
}
```

### 7. 桥接模式（Bridge Pattern）
将抽象部分与实现部分分离，使它们都可以独立地变化。

```java
public interface Implementor {
    void operationImpl();
}

public abstract class Abstraction {
    protected Implementor implementor;
    
    public Abstraction(Implementor implementor) {
        this.implementor = implementor;
    }
    
    public abstract void operation();
}
```

### 8. 组合模式（Composite Pattern）
将对象组合成树形结构以表示"部分-整体"的层次结构。

```java
public abstract class Component {
    public abstract void operation();
    public abstract void add(Component component);
    public abstract void remove(Component component);
}

public class Leaf extends Component {
    @Override
    public void operation() {
        System.out.println("Leaf operation");
    }
    
    @Override
    public void add(Component component) {
        throw new UnsupportedOperationException();
    }
    
    @Override
    public void remove(Component component) {
        throw new UnsupportedOperationException();
    }
}
```

### 9. 装饰器模式（Decorator Pattern）
动态地给一个对象添加一些额外的职责。

```java
public interface Component {
    void operation();
}

public class ConcreteComponent implements Component {
    @Override
    public void operation() {
        System.out.println("ConcreteComponent operation");
    }
}

public class Decorator implements Component {
    protected Component component;
    
    public Decorator(Component component) {
        this.component = component;
    }
    
    @Override
    public void operation() {
        component.operation();
    }
}
```

### 10. 外观模式（Facade Pattern）
为子系统中的一组接口提供一个一致的界面。

```java
public class Facade {
    private SubSystemA subSystemA;
    private SubSystemB subSystemB;
    
    public Facade() {
        subSystemA = new SubSystemA();
        subSystemB = new SubSystemB();
    }
    
    public void operation() {
        subSystemA.operationA();
        subSystemB.operationB();
    }
}
```

### 11. 享元模式（Flyweight Pattern）
运用共享技术有效地支持大量细粒度的对象。

```java
public class FlyweightFactory {
    private Map<String, Flyweight> flyweights = new HashMap<>();
    
    public Flyweight getFlyweight(String key) {
        Flyweight flyweight = flyweights.get(key);
        if (flyweight == null) {
            flyweight = new ConcreteFlyweight();
            flyweights.put(key, flyweight);
        }
        return flyweight;
    }
}
```

### 12. 代理模式（Proxy Pattern）
为其他对象提供一种代理以控制对这个对象的访问。

```java
public interface Subject {
    void request();
}

public class RealSubject implements Subject {
    @Override
    public void request() {
        System.out.println("RealSubject request");
    }
}

public class Proxy implements Subject {
    private RealSubject realSubject;
    
    @Override
    public void request() {
        if (realSubject == null) {
            realSubject = new RealSubject();
        }
        realSubject.request();
    }
}
```

## 行为型模式（11种）

### 13. 责任链模式（Chain of Responsibility Pattern）
使多个对象都有机会处理请求，从而避免请求的发送者和接收者之间的耦合关系。

```java
public abstract class Handler {
    protected Handler successor;
    
    public void setSuccessor(Handler successor) {
        this.successor = successor;
    }
    
    public abstract void handleRequest(Request request);
}
```

### 14. 命令模式（Command Pattern）
将一个请求封装为一个对象，从而使你可用不同的请求对客户进行参数化。

```java
public interface Command {
    void execute();
}

public class ConcreteCommand implements Command {
    private Receiver receiver;
    
    public ConcreteCommand(Receiver receiver) {
        this.receiver = receiver;
    }
    
    @Override
    public void execute() {
        receiver.action();
    }
}
```

### 15. 解释器模式（Interpreter Pattern）
给定一个语言，定义它的文法的一种表示，并定义一个解释器。

```java
public interface Expression {
    boolean interpret(String context);
}

public class TerminalExpression implements Expression {
    @Override
    public boolean interpret(String context) {
        // 实现终结符解释操作
        return true;
    }
}
```

### 16. 迭代器模式（Iterator Pattern）
提供一种方法顺序访问一个聚合对象中的各个元素，而又不暴露其内部的表示。

```java
public interface Iterator {
    boolean hasNext();
    Object next();
}

public class ConcreteIterator implements Iterator {
    private List<Object> list;
    private int index = 0;
    
    public ConcreteIterator(List<Object> list) {
        this.list = list;
    }
    
    @Override
    public boolean hasNext() {
        return index < list.size();
    }
    
    @Override
    public Object next() {
        return list.get(index++);
    }
}
```

### 17. 中介者模式（Mediator Pattern）
用一个中介对象来封装一系列的对象交互。

```java
public abstract class Mediator {
    public abstract void colleagueChanged(Colleague colleague);
}

public class ConcreteMediator extends Mediator {
    private Colleague colleague1;
    private Colleague colleague2;
    
    public void setColleague1(Colleague colleague1) {
        this.colleague1 = colleague1;
    }
    
    public void setColleague2(Colleague colleague2) {
        this.colleague2 = colleague2;
    }
    
    @Override
    public void colleagueChanged(Colleague colleague) {
        // 处理同事对象的变化
    }
}
```

### 18. 备忘录模式（Memento Pattern）
在不破坏封装性的前提下，捕获一个对象的内部状态，并在该对象之外保存这个状态。

```java
public class Memento {
    private String state;
    
    public Memento(String state) {
        this.state = state;
    }
    
    public String getState() {
        return state;
    }
}

public class Originator {
    private String state;
    
    public Memento createMemento() {
        return new Memento(state);
    }
    
    public void restoreMemento(Memento memento) {
        state = memento.getState();
    }
}
```

### 19. 观察者模式（Observer Pattern）
定义对象间的一种一对多的依赖关系，当一个对象的状态发生改变时，所有依赖于它的对象都得到通知并被自动更新。

```java
public interface Observer {
    void update();
}

public class Subject {
    private List<Observer> observers = new ArrayList<>();
    
    public void attach(Observer observer) {
        observers.add(observer);
    }
    
    public void notifyObservers() {
        for (Observer observer : observers) {
            observer.update();
        }
    }
}
```

### 20. 状态模式（State Pattern）
允许一个对象在其内部状态改变时改变它的行为。

```java
public interface State {
    void handle();
}

public class Context {
    private State state;
    
    public void setState(State state) {
        this.state = state;
    }
    
    public void request() {
        state.handle();
    }
}
```

### 21. 策略模式（Strategy Pattern）
定义一系列的算法，把它们一个个封装起来，并且使它们可相互替换。

```java
public interface Strategy {
    void algorithmInterface();
}

public class Context {
    private Strategy strategy;
    
    public Context(Strategy strategy) {
        this.strategy = strategy;
    }
    
    public void contextInterface() {
        strategy.algorithmInterface();
    }
}
```

### 22. 模板方法模式（Template Method Pattern）
定义一个操作中的算法的骨架，而将一些步骤延迟到子类中。

```java
public abstract class AbstractClass {
    public final void templateMethod() {
        primitiveOperation1();
        primitiveOperation2();
    }
    
    protected abstract void primitiveOperation1();
    protected abstract void primitiveOperation2();
}
```

### 23. 访问者模式（Visitor Pattern）
表示一个作用于某对象结构中的各元素的操作。

```java
public interface Visitor {
    void visit(ConcreteElementA element);
    void visit(ConcreteElementB element);
}

public interface Element {
    void accept(Visitor visitor);
}

public class ConcreteElementA implements Element {
    @Override
    public void accept(Visitor visitor) {
        visitor.visit(this);
    }
}
```

## 设计模式的使用建议

1. 不要过度使用设计模式，应该根据实际需求选择合适的模式
2. 理解每个设计模式的适用场景和优缺点
3. 在实际项目中，设计模式往往是组合使用的
4. 保持代码的简洁性和可维护性
5. 遵循SOLID原则 

## Spring框架中的设计模式应用

Spring框架大量使用了设计模式，以下是Spring中最常用的设计模式及其应用示例：

### 1. 单例模式（Singleton Pattern）
Spring默认使用单例模式管理Bean，通过IoC容器实现。

```java
@Component
public class UserService {
    // Spring容器会自动管理这个Bean为单例
    public void doSomething() {
        // 业务逻辑
    }
}
```

### 2. 工厂模式（Factory Pattern）
Spring使用BeanFactory和ApplicationContext作为Bean的工厂。

```java
@Configuration
public class AppConfig {
    @Bean
    public UserService userService() {
        return new UserServiceImpl();
    }
}
```

### 3. 代理模式（Proxy Pattern）
Spring AOP使用动态代理实现横切关注点。

```java
@Aspect
@Component
public class LoggingAspect {
    @Before("execution(* com.example.service.*.*(..))")
    public void logBefore(JoinPoint joinPoint) {
        System.out.println("Before method: " + joinPoint.getSignature().getName());
    }
}
```

### 4. 观察者模式（Observer Pattern）
Spring的事件机制使用观察者模式。

```java
@Component
public class UserEventListener implements ApplicationListener<UserCreatedEvent> {
    @Override
    public void onApplicationEvent(UserCreatedEvent event) {
        // 处理用户创建事件
    }
}

// 发布事件
@Component
public class UserService {
    @Autowired
    private ApplicationEventPublisher eventPublisher;
    
    public void createUser() {
        // 创建用户逻辑
        eventPublisher.publishEvent(new UserCreatedEvent(this));
    }
}
```

### 5. 模板方法模式（Template Method Pattern）
Spring的JdbcTemplate等模板类使用此模式。

```java
@Service
public class UserService {
    @Autowired
    private JdbcTemplate jdbcTemplate;
    
    public User findUser(Long id) {
        return jdbcTemplate.queryForObject(
            "SELECT * FROM users WHERE id = ?",
            (rs, rowNum) -> new User(rs.getLong("id"), rs.getString("name")),
            id
        );
    }
}
```

### 6. 适配器模式（Adapter Pattern）
Spring MVC中的HandlerAdapter使用此模式。

```java
@Controller
public class UserController {
    @RequestMapping("/users")
    public ResponseEntity<List<User>> getUsers() {
        // 处理请求并返回响应
        return ResponseEntity.ok(userService.findAll());
    }
}
```

### 7. 装饰器模式（Decorator Pattern）
Spring的TransactionManager等使用此模式。

```java
@Service
public class UserService {
    @Transactional
    public void createUser(User user) {
        // 事务管理通过装饰器模式实现
        userRepository.save(user);
    }
}
```

### 8. 策略模式（Strategy Pattern）
Spring的缓存抽象使用此模式。

```java
@Configuration
@EnableCaching
public class CacheConfig {
    @Bean
    public CacheManager cacheManager() {
        return new ConcurrentMapCacheManager("users");
    }
}

@Service
public class UserService {
    @Cacheable("users")
    public User findUser(Long id) {
        return userRepository.findById(id);
    }
}
```

### Spring设计模式使用建议

1. 理解Spring框架中设计模式的应用场景
2. 合理使用Spring提供的注解和配置
3. 遵循Spring的最佳实践
4. 注意性能影响，如单例模式的使用
5. 保持代码的可测试性和可维护性 