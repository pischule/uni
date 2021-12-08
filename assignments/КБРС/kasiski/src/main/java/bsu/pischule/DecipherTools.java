package bsu.pischule;

import org.apache.commons.lang3.StringUtils;
import org.apache.commons.lang3.tuple.Pair;

import java.util.*;
import java.util.function.Function;
import java.util.stream.Collectors;
import java.util.stream.IntStream;
import java.util.stream.Stream;

public class DecipherTools {

    public static int findKeyLength(String text) {
        return kasiskiExactCase(text.toLowerCase());
    }

    private static int kasiskiExactCase(String text) {
        Stream<String> substrings = IntStream
                .rangeClosed(3, 3)
                .parallel()
                .mapToObj(length -> findSubstringsWithoutSpaces(text, length))
                .flatMap(Collection::stream)
                .filter(it -> StringUtils.countMatches(text, it) > 1);

        List<Integer> distances = substrings
                .map(it -> occurrenceDistances(text, it))
                .flatMap(Collection::stream)
                .collect(Collectors.toList());

        Map<Integer, Long> gcdCounts = generatePairs(distances).parallelStream()
                .map(it -> gcd(it.getLeft(), it.getRight()))
                .collect(Collectors.groupingBy(Function.identity(), Collectors.counting()));

        return gcdCounts.entrySet().stream()
                .max(Comparator.comparingLong(Map.Entry::getValue))
                .map(Map.Entry::getKey)
                .orElse(1);
    }

    private static Set<String> findSubstringsWithoutSpaces(String text, int length) {
        if (text.length() < length) {
            throw new IllegalArgumentException("Text length should be longer than text length");
        }

        Set<String> substrings = new HashSet<>();
        for (int i = 0; i <= text.length() - length; ++i) {
            String substring = text.substring(i, i + length);
            if (substring.contains(" ")) continue;
            substrings.add(substring);
        }

        return substrings;
    }

    private static List<Integer> findSubstringPositions(String text, String substring) {
        List<Integer> indexes = new ArrayList<>();
        int wordLength = 0;
        int index = 0;
        while (index != -1) {
            index = text.indexOf(substring, index + wordLength);
            if (index != -1) {
                indexes.add(index);
            }
            wordLength = substring.length();
        }
        return indexes;
    }

    private static List<Pair<Integer, Integer>> generatePairs(Collection<Integer> elements) {
        List<Pair<Integer, Integer>> pairs = new ArrayList<>();
        ArrayList<Integer> elementsList = new ArrayList<>(elements);
        for (int i = 0; i < elements.size(); ++i) {
            for (int j = 0; j < i; ++j) {
                pairs.add(Pair.of(elementsList.get(i), elementsList.get(j)));
            }
        }
        return pairs;
    }

    private static List<Integer> occurrenceDistances(String text, String substring) {
        List<Integer> positions = findSubstringPositions(text, substring);
        return generatePairs(positions).stream()
                .map(it -> Math.abs(it.getLeft() - it.getRight()))
                .collect(Collectors.toList());
    }

    private static int gcd(int a, int b) {
        if (b == 0) return a;
        return gcd(b, a % b);
    }
}
