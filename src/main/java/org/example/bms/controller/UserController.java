package org.example.bms.controller;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.example.bms.dto.UserDto;
import org.example.bms.service.UserService;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/users")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;
    @GetMapping("/me")
    public ResponseEntity<UserDto> getCurrentUser() {

        String email =
                SecurityContextHolder
                        .getContext()
                        .getAuthentication()
                        .getName();

        return ResponseEntity.ok(
                userService.getUserByEmail(email));
    }

    @GetMapping("/{userId}")
    public ResponseEntity<UserDto> getUserById(
            @PathVariable Long userId) {

        return ResponseEntity.ok(
                userService.getUserById(userId)
        );
    }

    @PutMapping("/{userId}")
    public ResponseEntity<UserDto> updateUser(@PathVariable Long userId, @Valid @RequestBody UserDto userDto) {

        return ResponseEntity.ok(
                userService.updateUser(userId, userDto)
        );
    }

    @DeleteMapping("/{userId}")
    public ResponseEntity<UserDto> deleteUser(
            @PathVariable Long userId) {

        return ResponseEntity.ok(
                userService.deleteUser(userId)
        );
    }
}
