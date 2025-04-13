package bsu.pischule.encryptednotes.service;

import lombok.extern.slf4j.Slf4j;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import javax.crypto.SecretKey;
import javax.crypto.spec.IvParameterSpec;
import java.util.Base64;

@Slf4j
@SpringBootTest(classes = {EncryptionService.class})
class NotesServiceTest {

    @Autowired
    EncryptionService encryptionService;

    @Test
    public void encrypt() {
        SecretKey secretKey = encryptionService.getSessionKey(Base64.getDecoder().decode("MP1WdsrMxpV1hNVLWZ2RgA=="));
        IvParameterSpec iv = new IvParameterSpec(Base64.getDecoder().decode("TzCPfbR9peAO0wMdMTtXkQ=="));
        log.info("key: {}", Base64.getEncoder().encodeToString(secretKey.getEncoded()));
        log.info("iv: {}", Base64.getEncoder().encodeToString(iv.getIV()));
        byte[] bytes = encryptionService.encryptAes("123", secretKey, iv);
        log.info(Base64.getEncoder().encodeToString(bytes));

    }
}