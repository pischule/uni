package bsu.pischule.cipherbreakers;

import bsu.pischule.ciphers.Caesar;

import java.util.Comparator;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

import static bsu.pischule.ResourceHelpers.loadAlphabet;
import static bsu.pischule.ResourceHelpers.loadLetterFrequency;

public class CaesarCipherBreaker implements CipherBreaker {
    private final Map<String, Double> languageLetterFrequency;
    private final String alphabet;
    private final Caesar caesar;

    public CaesarCipherBreaker(String language) {
        languageLetterFrequency = loadLetterFrequency(language);
        alphabet = loadAlphabet(language);
        caesar = new Caesar(alphabet, 0);
    }

    @Override
    public String decrypt(String text) {
        return IntStream.range(0, alphabet.length())
                .mapToObj(shift -> caesar.decrypt(text, shift))
                .min(Comparator.comparingDouble(it -> letterFrequencyDifference(
                        calculateLetterFrequencies(it)
                ))).orElseThrow();
    }

    private Map<String, Double> calculateLetterFrequencies(String text) {
        Map<String, Long> textLetterCounts = text.chars()
                .map(Character::toLowerCase)
                .mapToObj(Character::toString)
                .filter(alphabet::contains)
                .collect(Collectors.groupingBy(Function.identity(), Collectors.counting()));
        return textLetterCounts.entrySet().stream()
                .collect(Collectors.toMap(Map.Entry::getKey, it -> it.getValue() * 1.0 / text.length()));
    }

    private Double letterFrequencyDifference(Map<String, Double> letterFrequency) {
        return letterFrequency.entrySet().stream()
                .map(it -> languageLetterFrequency.get(it.getKey()) - it.getValue())
                .mapToDouble(it -> it * it).sum();
    }
}
