package org.example.bms.controller;

import lombok.RequiredArgsConstructor;
import org.example.bms.dto.UserDto;
import org.example.bms.service.UserService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/users")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    @GetMapping("/{userId}")
    public ResponseEntity<UserDto> getUserById(
            @PathVariable Long userId) {

        return ResponseEntity.ok(
                userService.getUserById(userId)
        );
    }

    @PutMapping("/{userId}")
    public ResponseEntity<UserDto> updateUser(
            @PathVariable Long userId,
            @RequestBody UserDto userDto) {

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
