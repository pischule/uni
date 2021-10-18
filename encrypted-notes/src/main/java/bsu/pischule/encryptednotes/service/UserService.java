package bsu.pischule.encryptednotes.service;

import bsu.pischule.encryptednotes.configuration.AppConfig;
import bsu.pischule.encryptednotes.dto.SessionKeyRequest;
import bsu.pischule.encryptednotes.dto.SessionKeyResponse;
import bsu.pischule.encryptednotes.entity.User;
import bsu.pischule.encryptednotes.exception.AuthorizationException;
import bsu.pischule.encryptednotes.exception.EncryptionException;
import bsu.pischule.encryptednotes.repository.UserRepository;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.PBEKeySpec;
import javax.persistence.EntityNotFoundException;
import javax.transaction.Transactional;
import java.security.NoSuchAlgorithmException;
import java.security.PublicKey;
import java.security.SecureRandom;
import java.security.spec.InvalidKeySpecException;
import java.security.spec.KeySpec;
import java.time.Duration;
import java.time.Instant;
import java.util.Arrays;
import java.util.List;
import java.util.UUID;

@AllArgsConstructor
@Service
public class UserService {
    private EncryptionService encryptionService;
    private UserRepository userRepository;
    private AppConfig config;

    @Transactional
    public SessionKeyResponse getSessionKey(SessionKeyRequest request) {
        User user = userRepository.findByUsername(request.username()).orElseThrow(() -> new EntityNotFoundException("no such user"));
        if (!userPasswordMatches(user, request.password())) {
            throw new AuthorizationException("incorrect password");
        }

        if (keyHasExpired(user)) {
            renewSession(user);
        }

        PublicKey publicKey = encryptionService.readPublicKey(request.publicKeyPem());
        byte[] encryptedSessionKey = encryptionService.encryptRsa(user.getSessionKey(), publicKey);

        return new SessionKeyResponse(encryptedSessionKey, user.getSessionToken());
    }

    public User getAndCheckUserBySessionToken(UUID sessionToken) {
        User user = userRepository.findBySessionToken(sessionToken)
                .orElseThrow(() -> new EntityNotFoundException("user not found"));
        if (Instant.now().isAfter(user.getSessionExpirationDate())) {
            throw new AuthorizationException("session key has expired");
        }
        return user;
    }

    public boolean userPasswordMatches(User user, String comparedPassword) {
        try {
            return Arrays.equals(user.getPasswordHash(), hashPassword(comparedPassword, user.getPasswordSalt()));
        } catch (NoSuchAlgorithmException | InvalidKeySpecException e) {
            e.printStackTrace();
            return false;
        }
    }

    public User buildUser(String username, String password) {
        try {
            byte[] salt = generateSalt();
            byte[] passwordHash = hashPassword(password, salt);
            byte[] sessionKey = encryptionService.generateAesKey().getEncoded();
            Instant sessionExpirationDate = Instant.now().plus(getSessionTtl());
            return new User(null, username, passwordHash, salt, sessionKey, UUID.randomUUID(), sessionExpirationDate, List.of());
        } catch (NoSuchAlgorithmException | InvalidKeySpecException e) {
            e.printStackTrace();
            throw new EncryptionException("error while password hashing");
        }
    }

    @Transactional
    public void renewSession(User user) {
        byte[] sessionKey = encryptionService.generateAesKey().getEncoded();
        user.setSessionKey(sessionKey);
        user.setSessionExpirationDate(Instant.now().plus(getSessionTtl()));
        user.setSessionToken(UUID.randomUUID());
        userRepository.save(user);
    }

    public boolean keyHasExpired(User user) {
        return Instant.now().isAfter(user.getSessionExpirationDate());
    }

    private byte[] hashPassword(String password, byte[] salt) throws NoSuchAlgorithmException, InvalidKeySpecException {
        KeySpec spec = new PBEKeySpec(password.toCharArray(), salt, 65536, 128);
        SecretKeyFactory factory = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA1");
        return factory.generateSecret(spec).getEncoded();
    }

    private Duration getSessionTtl() {
        return Duration.ofDays(config.sessionTtlDays);
    }

    private byte[] generateSalt() {
        SecureRandom random = new SecureRandom();
        byte[] salt = new byte[16];
        random.nextBytes(salt);
        return salt;
    }

}
