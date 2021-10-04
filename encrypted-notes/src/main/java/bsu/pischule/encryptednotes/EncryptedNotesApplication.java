package bsu.pischule.encryptednotes;

import bsu.pischule.encryptednotes.entity.Note;
import bsu.pischule.encryptednotes.entity.User;
import bsu.pischule.encryptednotes.repository.NoteRepository;
import bsu.pischule.encryptednotes.repository.UserRepository;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

@Slf4j
@SpringBootApplication
@AllArgsConstructor
public class EncryptedNotesApplication {
    private final UserRepository userRepository;
    private final NoteRepository noteRepository;

    public static void main(String[] args) {
        SpringApplication.run(EncryptedNotesApplication.class, args);
    }

    @Bean
    CommandLineRunner commandLineRunner() {
        return args -> {
            String text = """
                    Твой батя моему в подметки не годится. Мой ебашит вообще адовые блюда. Ну такой вот примерно рецепт\
                     усредненный, потому что вариаций масса. Берется суп, он не греется, греть – это не про моего батю. Он \
                     берет это суп, вываливает его на сковороду и начинает жарить. Добавляет в него огромное количество \
                     лука, чеснока, перца черного и красного МУКИ! для вязкости, томатная паста сверху. Все это жарится \
                     до дыма. Потом снимается с огня и остужается на балконе. Потом батя заносит и щедро полив майонезом \
                     начинает есть. При этом ест со сковороды шкрябая по ней ложкой. Ест и приговаривает полушепотом ух\
                      бля. При этом у него на лбу аж пот выступает. Любезно мне иногда предлагает, но я отказываюсь. Надо \
                      ли говорить о том какой дичайший пердеж потом? Вонища такая, что обои от стен отклеиваются.""";
            Note note = new Note(1L, text);
            noteRepository.save(note);
            log.info("Note saved: {}", note);

            User user = new User(1L, null);
            userRepository.save(user);
            log.info("User saved: {}", user);
        };
    }

}
