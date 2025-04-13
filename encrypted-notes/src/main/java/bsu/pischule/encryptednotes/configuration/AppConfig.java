package bsu.pischule.encryptednotes.configuration;


import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;

@Data
@ConfigurationProperties(prefix = "app")
public class AppConfig {
    public String dbEncryptionKey;
    public String dbEncryptionIv;
    public Long sessionTtlDays;
}
