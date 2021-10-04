package bsu.pischule.encryptednotes.repository;

import bsu.pischule.encryptednotes.entity.Note;
import org.springframework.data.jpa.repository.JpaRepository;

public interface NoteRepository extends JpaRepository<Note, Long> {
}
