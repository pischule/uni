package bsu.pischule.cipherbreakers;

import bsu.pischule.DecipherTools;

import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

public class VigenerCipherBreaker implements CipherBreaker {
    private final CaesarCipherBreaker caesarCipherBreaker;

    public VigenerCipherBreaker(String language) {
        caesarCipherBreaker = new CaesarCipherBreaker(language);
    }

    @Override
    public String decrypt(String text) {
        int keyLength = DecipherTools.findKeyLength(text);
        return decrypt(text, keyLength);
    }

    public String decrypt(String text, int keyLength) {
        List<String> slicedText = unzipStrings(text, keyLength);
        List<String> decryptedSlices = slicedText.parallelStream()
                .map(caesarCipherBreaker::decrypt)
                .collect(Collectors.toList());
        return zipStrings(decryptedSlices);
    }

    private String zipStrings(List<String> slices) {
        StringBuilder sb = new StringBuilder();
        int resultLength = slices.stream().mapToInt(String::length).sum();
        for (int i = 0; i < resultLength; ++i) {
            sb.append(slices.get(i % slices.size()).charAt(i / slices.size()));
        }
        return sb.toString();
    }

    private List<String> unzipStrings(String text, int keyLength) {
        List<StringBuilder> stringBuilders = IntStream.range(0, keyLength)
                .mapToObj(StringBuilder::new)
                .collect(Collectors.toList());

        for (int i = 0; i < text.length(); ++i) {
            stringBuilders.get(i % keyLength).append(text.charAt(i));
        }

        return stringBuilders.stream()
                .map(StringBuilder::toString)
                .collect(Collectors.toList());
    }
}
