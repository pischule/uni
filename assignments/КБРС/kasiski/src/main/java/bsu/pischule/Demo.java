package bsu.pischule;

import bsu.pischule.cipherbreakers.VigenerCipherBreaker;
import bsu.pischule.ciphers.Vigenere;

import java.util.HashMap;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

import static bsu.pischule.ResourceHelpers.loadAlphabet;
import static bsu.pischule.ResourceHelpers.loadResource;

public class Demo {
    public static void main(String[] args) {
        demo1();
        demo2();
    }

    public static void demo1() {
        var numberOfSamples = 10;
        // 10 30 50.. 1000
        List<Integer> textLengths = IntStream.rangeClosed(1, 100).mapToObj(it -> it * 10).collect(Collectors.toList());

        var alphabet = loadAlphabet("russian");
        var allText = loadResource("text/451.txt");

        int offset = 0;
        var textLengthToDecryptionFrequency = new HashMap<Integer, Double>();
        System.out.println("by text length:");
        for (var textLength : textLengths) {
            System.out.print(textLength + " ");
            for (int i = 0; i < numberOfSamples; ++i) {
                var text = allText.substring(offset, offset + textLength);
                var encrypted = new Vigenere(alphabet, "бредбери").encrypt(text);
                var decrypted = new VigenerCipherBreaker("russian").decrypt(encrypted);

                var oldFrequency = textLengthToDecryptionFrequency.getOrDefault(textLength, 0.0);
                textLengthToDecryptionFrequency.put(textLength, oldFrequency + (stringMatch(decrypted, text)) / numberOfSamples);

                offset += textLength;
                if (offset + textLength > allText.length()) {
                    offset = 0;
                }
            }
        }

        System.out.println("\nstats: ");
        textLengthToDecryptionFrequency.entrySet()
                .stream()
                .sorted(java.util.Map.Entry.comparingByKey())
                .forEach(it -> System.out.printf("%d,%.4f%n", it.getKey(), it.getValue()));

    }

    public static void demo2() {
        var numberOfSamples = 10;
        var textLength = 500;
        String longestPassword = "четырестапятьдесятодинградусовпофаренгейту";
        var keys = IntStream.range(1, longestPassword.length() / 2)
                .mapToObj(it -> longestPassword.substring(0, it * 2))
                .collect(Collectors.toList());

        var alphabet = loadAlphabet("russian");
        var allText = loadResource("text/451.txt");

        int offset = 0;
        var textLengthToDecryptionFrequency = new HashMap<Integer, Double>();
        System.out.println("by password length:");
        for (var key : keys) {
            System.out.print(key.length() + " ");
            for (int i = 0; i < numberOfSamples; ++i) {
                var text = allText.substring(offset, offset + textLength);
                var encrypted = new Vigenere(alphabet, key).encrypt(text);
                var decrypted = new VigenerCipherBreaker("russian").decrypt(encrypted);

                var oldFrequency = textLengthToDecryptionFrequency.getOrDefault(key.length(), 0.0);
                textLengthToDecryptionFrequency.put(key.length(), oldFrequency + (stringMatch(decrypted, text)) / numberOfSamples);

                offset += textLength;
                if (offset + textLength > allText.length()) {
                    offset = 0;
                }
            }
        }

        System.out.println("\nstats: ");
        textLengthToDecryptionFrequency.entrySet()
                .stream()
                .sorted(java.util.Map.Entry.comparingByKey())
                .forEach(it -> System.out.printf("%d,%.4f%n", it.getKey(), it.getValue()));
    }

    public static double stringMatch(String s1, String s2) {
        if (s2.length() != s1.length()) return 0;
        return IntStream.range(0, s1.length())
                .map(it -> s1.charAt(it) == s2.charAt(it) ? 1 : 0)
                .sum() * 1.0 / s1.length();
    }

}
