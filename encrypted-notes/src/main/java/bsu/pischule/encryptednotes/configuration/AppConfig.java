package bsu.pischule.encryptednotes.configuration;


import org.springframework.context.annotation.Configuration;

import java.time.Duration;

@Configuration
public class AppConfig {
    public Duration defaultSessionTtl() {
        return Duration.ofDays(10);
    }
}
