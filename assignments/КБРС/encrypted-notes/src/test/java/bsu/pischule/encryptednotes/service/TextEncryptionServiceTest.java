package bsu.pischule.encryptednotes.service;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

@Slf4j
@SpringBootTest(classes = {EncryptionService.class})
class TextEncryptionServiceTest {
    @Autowired
    EncryptionService encryptionService;
}