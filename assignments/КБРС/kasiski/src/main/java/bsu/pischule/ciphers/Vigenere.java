package bsu.pischule.ciphers;


import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

public class Vigenere implements Cipher {
    private final List<Integer> alphabetLetters;
    private final List<Integer> shifts;
    private final Map<Integer, Integer> charToPositionMapping;

    public Vigenere(String alphabet, String key) {
        if (!lettersAreUnique(alphabet) || !keyConsistsOfLetters(alphabet, key)) {
            throw new IllegalArgumentException("Alphabet should not contain repeating letters and alphabet should contain all key letters");
        }

        this.alphabetLetters = alphabet.chars().boxed().map(Character::toLowerCase).collect(Collectors.toList());
        this.charToPositionMapping = IntStream
                .range(0, alphabet.length())
                .boxed()
                .collect(Collectors.toMap(alphabetLetters::get, it -> it));
        this.shifts = key.chars()
                .boxed()
                .map(charToPositionMapping::get)
                .collect(Collectors.toList());
    }

    private static boolean lettersAreUnique(String alphabet) {
        return alphabet.chars()
                .mapToObj(Character::toLowerCase)
                .distinct()
                .count() == alphabet.length();
    }

    @Override
    public String encrypt(String text) {
        List<Integer> sourceLetters = text.chars().boxed().collect(Collectors.toList());
        return IntStream.range(0, sourceLetters.size())
                .mapToObj(it -> shiftCharacter(sourceLetters.get(it), shifts.get(it % shifts.size())))
                .map(Character::toString)
                .collect(Collectors.joining());
    }

    @Override
    public String decrypt(String text) {
        List<Integer> sourceLetters = text.chars().boxed().collect(Collectors.toList());
        return IntStream.range(0, text.length())
                .mapToObj(it -> shiftCharacter(sourceLetters.get(it), -shifts.get(it % shifts.size())))
                .map(Character::toString)
                .collect(Collectors.joining());
    }

    private Integer shiftCharacter(Integer letter, int letterShift) {
        int letterInLowerCase = Character.toLowerCase(letter);
        if (charToPositionMapping.containsKey(letterInLowerCase)) {
            int oldCharPosition = charToPositionMapping.get(letterInLowerCase);
            int newPosition = ((alphabetLetters.size() + oldCharPosition + letterShift) % alphabetLetters.size());
            int newLetterLowerCase = alphabetLetters.get(newPosition);
            return Character.isUpperCase(letter) ? Character.toUpperCase(newLetterLowerCase) : newLetterLowerCase;
        } else {
            return letter;
        }
    }

    private static boolean keyConsistsOfLetters(String alphabet, String key) {
        Set<Integer> allowedLetters = alphabet.chars()
                .boxed()
                .collect(Collectors.toSet());
        return key.chars()
                .allMatch(allowedLetters::contains);
    }
}
