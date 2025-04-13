package bsu.pischule;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.common.io.Resources;
import lombok.SneakyThrows;

import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.Map;

public class ResourceHelpers {
    private static final ObjectMapper objectMapper = new ObjectMapper();

    @SneakyThrows
    public static String loadResource(String resourceName) {
        URL url = Resources.getResource(resourceName);
        return Resources.toString(url, StandardCharsets.UTF_8);
    }

    @SneakyThrows
    public static Map<String, Double> loadLetterFrequency(String language) {
        String path = "languages/%s.json".formatted(language);
        String resource = loadResource(path);
        return objectMapper.readValue(resource, new TypeReference<>() {
        });
    }

    public static String loadAlphabet(String language) {
        return String.join("", loadLetterFrequency(language).keySet()).toLowerCase();
    }

}
