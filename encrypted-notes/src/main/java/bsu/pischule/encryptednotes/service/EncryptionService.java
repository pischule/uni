package bsu.pischule.encryptednotes.service;

import org.springframework.stereotype.Service;

@Service
public class EncryptionService {
    public String generateSessionKey() {
        return "amogus";
    }

    public String encryptText(String text, String key) {
        return text;
    }
}
