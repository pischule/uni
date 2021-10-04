package bsu.pischule.encryptednotes.repository;

import bsu.pischule.encryptednotes.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;

public interface UserRepository extends JpaRepository<User, Long> {
}
