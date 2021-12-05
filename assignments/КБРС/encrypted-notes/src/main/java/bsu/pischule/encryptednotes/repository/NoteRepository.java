package bsu.pischule.encryptednotes.repository;

import bsu.pischule.encryptednotes.entity.Note;
import bsu.pischule.encryptednotes.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

public interface NoteRepository extends JpaRepository<Note, UUID> {
    List<Note> findAllByUser(User user);

    Optional<Note> findByIdAndUser(UUID id, User user);

    void deleteByIdAndUser(UUID id, User user);
}
