package bsu.pischule.encryptednotes.entity;

import lombok.*;
import org.hibernate.Hibernate;

import javax.persistence.*;
import java.time.Instant;
import java.util.List;
import java.util.Objects;
import java.util.UUID;

@Getter
@Setter
@ToString
@AllArgsConstructor
@NoArgsConstructor
@Entity
public class User {
    @Id
    @GeneratedValue
    private UUID id;
    @Column(unique = true)
    private String username;
    private byte[] passwordHash;
    private byte[] passwordSalt;

    @Lob
    private byte[] sessionKey;
    @Column(unique = true)
    private UUID sessionToken;
    private Instant sessionExpirationDate;

    @OneToMany(fetch = FetchType.LAZY, mappedBy = "user")
    @ToString.Exclude
    private List<Note> notes = List.of();

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || Hibernate.getClass(this) != Hibernate.getClass(o)) return false;
        User user = (User) o;
        return Objects.equals(id, user.id);
    }

    @Override
    public int hashCode() {
        return 0;
    }
}
