package bsu.pischule.ciphers;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

public class Caesar implements Cipher {
    private final List<Integer> alphabetLetters;
    private final int shift;
    private final Map<Integer, Integer> charToPositionMapping;

    public Caesar(String alphabet, int shift) {
        if (!lettersAreUnique(alphabet)) {
            throw new IllegalArgumentException("Alphabet Letters are not unique");
        }

        this.alphabetLetters = alphabet.chars().boxed().map(Character::toLowerCase).collect(Collectors.toList());
        this.shift = shift;
        this.charToPositionMapping = IntStream
                .range(0, alphabet.length())
                .boxed()
                .collect(Collectors.toMap(alphabetLetters::get, it -> it));
    }

    private static boolean lettersAreUnique(String alphabet) {
        return alphabet.chars()
                .mapToObj(Character::toLowerCase)
                .distinct()
                .count() == alphabet.length();
    }

    @Override
    public String encrypt(String text) {
        return text.chars()
                .mapToObj(it -> shiftCharacter(it, shift))
                .map(Character::toString)
                .collect(Collectors.joining());
    }

    public String encrypt(String text, int shift) {
        return text.chars()
                .mapToObj(it -> shiftCharacter(it, shift))
                .map(Character::toString)
                .collect(Collectors.joining());
    }

    @Override
    public String decrypt(String text) {
        return text.chars()
                .mapToObj(it -> shiftCharacter(it, -shift))
                .map(Character::toString)
                .collect(Collectors.joining());
    }

    public String decrypt(String text, int shift) {
        return text.chars()
                .mapToObj(it -> shiftCharacter(it, -shift))
                .map(Character::toString)
                .collect(Collectors.joining());
    }

    private Integer shiftCharacter(Integer letter, int letterShift) {
        int letterInLowerCase = Character.toLowerCase(letter);
        if (charToPositionMapping.containsKey(letterInLowerCase)) {
            int oldCharPosition = charToPositionMapping.get(letterInLowerCase);
            int newPosition = (alphabetLetters.size() + oldCharPosition + letterShift) % alphabetLetters.size();
            int newLetterLowerCase = alphabetLetters.get(newPosition);
            return Character.isUpperCase(letter) ? Character.toUpperCase(newLetterLowerCase) : newLetterLowerCase;
        } else {
            return letter;
        }
    }
}
