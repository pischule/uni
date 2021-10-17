package bsu.pischule.encryptednotes.entity;

import bsu.pischule.encryptednotes.configuration.AppConfig;
import bsu.pischule.encryptednotes.service.EncryptionService;
import lombok.AllArgsConstructor;

import javax.persistence.AttributeConverter;
import javax.persistence.Converter;

@Converter
@AllArgsConstructor
public class NoteTextConverter implements AttributeConverter<String, byte[]> {

    private final EncryptionService encryptionService;
    private final AppConfig appConfig;

    @Override
    public byte[] convertToDatabaseColumn(String s) {
        return encryptionService.encryptAes(
                s, appConfig.getInternalEncryptionKey(), appConfig.getInternalEncryptionIv());
    }

    @Override
    public String convertToEntityAttribute(byte[] bytes) {
        return encryptionService.decryptAes(bytes,
                appConfig.getInternalEncryptionKey(), appConfig.getInternalEncryptionIv());
    }
}
