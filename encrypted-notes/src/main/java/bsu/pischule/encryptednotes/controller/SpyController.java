package bsu.pischule.encryptednotes.controller;

import bsu.pischule.encryptednotes.dto.EncryptedNoteResponse;
import bsu.pischule.encryptednotes.dto.SessionKeyRequest;
import bsu.pischule.encryptednotes.dto.SessionKeyResponse;
import bsu.pischule.encryptednotes.service.EncryptionService;
import lombok.AllArgsConstructor;
import lombok.SneakyThrows;
import lombok.extern.slf4j.Slf4j;
import org.bouncycastle.openssl.jcajce.JcaPEMWriter;
import org.springframework.web.bind.annotation.*;

import javax.crypto.SecretKey;
import javax.crypto.spec.IvParameterSpec;
import java.io.IOException;
import java.io.StringWriter;
import java.security.KeyPair;
import java.security.PublicKey;
import java.util.*;

@Slf4j
@CrossOrigin
@AllArgsConstructor
@RestController
public class SpyController {
    private final EncryptionService encryptionService;
    private final SessionKeyController sessionKeyController;
    private final EncryptedNoteController encryptedNoteController;

    private static final Map<UUID, byte[]> keys = new HashMap<>();

    @SneakyThrows
    @PostMapping("/api/session-key/")
    public SessionKeyResponse spy(@RequestBody SessionKeyRequest request) {
        PublicKey theirPublic = encryptionService.readPublicKey(request.getPublicKeyPem());
        KeyPair ourKeyPair = encryptionService.generateKeyRsa();

        request.setPublicKeyPem(toPEM(ourKeyPair.getPublic()));

        SessionKeyResponse response = sessionKeyController.getSessionKey(request);
        byte[] ourEncryptedSessionKey = response.getEncryptedSessionKey();
        byte[] decryptedSessionKey = encryptionService.decryptRsa(ourEncryptedSessionKey, ourKeyPair.getPrivate());
        byte[] theirEncryptedSessionKey = encryptionService.encryptRsa(decryptedSessionKey, theirPublic);
        response.setEncryptedSessionKey(theirEncryptedSessionKey);

        keys.put(response.getSessionToken(), decryptedSessionKey);

        log.info("SessionKey: {}", Base64.getEncoder().encodeToString(decryptedSessionKey));

        return response;
    }

    @GetMapping("/api/note/")
    public List<EncryptedNoteResponse> getNotes(@RequestHeader("Authorization") UUID sessionToken) {

        List<EncryptedNoteResponse> theirEncryptedNotes = encryptedNoteController.getNotes(sessionToken);
        try {
            byte[] keyBytes = keys.get(sessionToken);
            SecretKey key = encryptionService.getSessionKey(keyBytes);

            log.info("notes of user with token: {}", sessionToken);
            theirEncryptedNotes.stream()
                    .map(n -> encryptionService.decryptAes(n.getEncryptedNote(), key, new IvParameterSpec(n.getIv())))
                    .forEach(text -> log.info("note: {}", text));

        } catch (NullPointerException ignored) {
        }
        return theirEncryptedNotes;
    }

    public static String toPEM(PublicKey pubKey) throws IOException {
        StringWriter sw = new StringWriter();
        JcaPEMWriter pemWriter = new JcaPEMWriter(sw);
        pemWriter.writeObject(pubKey);
        pemWriter.close();
        return sw.toString();
    }
}
