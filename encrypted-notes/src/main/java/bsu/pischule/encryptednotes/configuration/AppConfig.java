package bsu.pischule.encryptednotes.configuration;


import org.springframework.context.annotation.Configuration;

import javax.crypto.SecretKey;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import java.time.Duration;
import java.util.Base64;

@Configuration
public class AppConfig {
    public Duration defaultSessionTtl() {
        return Duration.ofDays(10);
    }

    public SecretKey getInternalEncryptionKey() {
        byte[] keyBytes = Base64.getDecoder().decode("YfV78Fg2TOsyUWaVPZt7lw==");
        return new SecretKeySpec(keyBytes, 0, keyBytes.length, "AES");
    }

    public IvParameterSpec getInternalEncryptionIv() {
        return new IvParameterSpec(Base64.getDecoder().decode("TzCPfbR9peAO0wMdMTtXkQ=="));
    }
}
