package bsu.pischule.encryptednotes.entity;

import bsu.pischule.encryptednotes.configuration.AppConfig;
import bsu.pischule.encryptednotes.service.EncryptionService;
import lombok.AllArgsConstructor;

import javax.crypto.SecretKey;
import javax.crypto.spec.IvParameterSpec;
import javax.persistence.AttributeConverter;
import javax.persistence.Converter;
import java.util.Base64;

@Converter
@AllArgsConstructor
public class NoteTextConverter implements AttributeConverter<String, byte[]> {

    private final EncryptionService encryptionService;
    private final AppConfig appConfig;

    @Override
    public byte[] convertToDatabaseColumn(String s) {
        return encryptionService.encryptAes(
                s, getKey(), getIv());
    }

    @Override
    public String convertToEntityAttribute(byte[] bytes) {
        return encryptionService.decryptAes(bytes, getKey(), getIv());
    }

    private SecretKey getKey() {
        return encryptionService.getSessionKey(Base64.getDecoder().decode(appConfig.dbEncryptionKey));
    }

    private IvParameterSpec getIv() {
        return new IvParameterSpec(Base64.getDecoder().decode(appConfig.dbEncryptionIv));
    }
}
