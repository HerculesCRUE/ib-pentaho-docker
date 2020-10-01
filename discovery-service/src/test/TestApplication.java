package es.um.asio.back.test;

import es.um.asio.back.controller.URISController;
import es.um.asio.service.mapper.MapperConfig;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Import;
import org.springframework.security.crypto.factory.PasswordEncoderFactories;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootApplication
@EnableAsync
@EnableAutoConfiguration
@Import(MapperConfig.class)
@ActiveProfiles("dev")
public class TestApplication {
    /**@SpringBootApplication
     @EnableAutoConfiguration
     @Import({ ServiceConfig.class })
     @ComponentScan
     * Main method for embedded deployment.
     *
     * @param args
     *            the arguments
     */

/*    @Bean("threadPoolExecutor")
    public Executor taskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(2);
        executor.setMaxPoolSize(2);
        executor.setQueueCapacity(500);
        executor.setThreadNamePrefix("GithubLookup-");
        executor.initialize();
        return executor;
    }*/

    public static void main(final String[] args) {
        SpringApplication.run(TestApplication.class, args);
    }

    /**
     * Creates the password encoder BCrypt.
     *
     * @return The password encoder.
     */
    @Bean
    public PasswordEncoder passwordEncoder() {
        return PasswordEncoderFactories.createDelegatingPasswordEncoder();
    }
}