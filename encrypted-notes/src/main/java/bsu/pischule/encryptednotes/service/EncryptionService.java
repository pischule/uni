package bsu.pischule.encryptednotes.service;

import bsu.pischule.encryptednotes.exception.EncryptionException;
import lombok.SneakyThrows;
import org.bouncycastle.util.io.pem.PemObject;
import org.bouncycastle.util.io.pem.PemReader;
import org.springframework.stereotype.Service;

import javax.crypto.*;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import java.io.IOException;
import java.io.StringReader;
import java.nio.charset.StandardCharsets;
import java.security.*;
import java.security.spec.InvalidKeySpecException;
import java.security.spec.X509EncodedKeySpec;

@Service
public class EncryptionService {
    private final String AES_ALGORITHM = "AES/CFB/NoPadding";

    public byte[] encryptAes(String input, SecretKey key, IvParameterSpec iv) {
        try {
            Cipher cipher = Cipher.getInstance(AES_ALGORITHM);
            cipher.init(Cipher.ENCRYPT_MODE, key, iv);
            return cipher.doFinal(input.getBytes(StandardCharsets.UTF_8));
        } catch (InvalidAlgorithmParameterException | NoSuchPaddingException | IllegalBlockSizeException | NoSuchAlgorithmException | BadPaddingException | InvalidKeyException e) {
            e.printStackTrace();
            throw new EncryptionException("aes encryption exception");
        }
    }

    public String decryptAes(byte[] plainText, SecretKey key, IvParameterSpec iv) {
        try {
            Cipher cipher = Cipher.getInstance(AES_ALGORITHM);
            cipher.init(Cipher.DECRYPT_MODE, key, iv);
            return new String(plainText);
        } catch (InvalidAlgorithmParameterException | NoSuchPaddingException | NoSuchAlgorithmException | InvalidKeyException e) {
            e.printStackTrace();
            throw new EncryptionException("aes decrypt exception");
        }
    }

    public SecretKey getSessionKey(byte[] encodedAesKey) {
        return new SecretKeySpec(encodedAesKey, 0, encodedAesKey.length, "AES");
    }

    public SecretKey generateAesKey() {
        try {
            KeyGenerator keyGenerator = KeyGenerator.getInstance("AES");
            keyGenerator.init(128);
            return keyGenerator.generateKey();
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
            throw new EncryptionException("cannot generate aes key");
        }
    }

    public IvParameterSpec generateIv() {
        byte[] iv = new byte[16];
        new SecureRandom().nextBytes(iv);
        return new IvParameterSpec(iv);
    }

    @SneakyThrows
    public byte[] encryptRsa(byte[] secretMessageBytes, PublicKey publicKey) {
        Cipher encryptCipher = Cipher.getInstance("RSA");
        encryptCipher.init(Cipher.ENCRYPT_MODE, publicKey);
        return encryptCipher.doFinal(secretMessageBytes);
    }

    @SneakyThrows
    public byte[] decryptRsa(byte[] encryptedBytes, PrivateKey publicKey) {
        Cipher encryptCipher = Cipher.getInstance("RSA");
        encryptCipher.init(Cipher.DECRYPT_MODE, publicKey);
        return encryptCipher.doFinal(encryptedBytes);
    }


    public KeyPair generateKeyRsa() throws NoSuchAlgorithmException {
        KeyPairGenerator generator = KeyPairGenerator.getInstance("RSA");
        generator.initialize(2048);
        return generator.generateKeyPair();
    }

    @SneakyThrows(NoSuchAlgorithmException.class)
    public PublicKey readPublicKey(String publicKeyPem) {
        KeyFactory factory = KeyFactory.getInstance("RSA");

        try (StringReader keyReader = new StringReader(publicKeyPem);
             PemReader pemReader = new PemReader(keyReader)) {

            PemObject pemObject = pemReader.readPemObject();
            byte[] content = pemObject.getContent();
            X509EncodedKeySpec pubKeySpec = new X509EncodedKeySpec(content);
            return factory.generatePublic(pubKeySpec);
        } catch (IOException | InvalidKeySpecException e) {
            e.printStackTrace();
            throw new EncryptionException("cannot parse public key");
        }
    }
}
