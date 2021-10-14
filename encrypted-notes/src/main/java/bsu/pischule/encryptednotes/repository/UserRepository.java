package bsu.pischule.encryptednotes.repository;

import bsu.pischule.encryptednotes.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;
import java.util.UUID;

public interface UserRepository extends JpaRepository<User, UUID> {
    Optional<User> findBySessionToken(UUID sessionToken);

    Optional<User> findByUsername(String username);
}
