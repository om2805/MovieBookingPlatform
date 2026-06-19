package org.example.bms.service;

import lombok.RequiredArgsConstructor;
import org.example.bms.dto.AuthResponseDto;
import org.example.bms.dto.LoginRequestDto;
import org.example.bms.dto.SignupRequestDto;
import org.example.bms.model.Role;
import org.example.bms.model.User;
import org.example.bms.repo.UserRepository;
import org.example.bms.security.JwtService;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
@Service
@RequiredArgsConstructor
public class AuthService {

    private final UserRepository userRepository;

    private final PasswordEncoder passwordEncoder;
    private final JwtService jwtService;

    private final AuthenticationManager
            authenticationManager;

    public String signup(
            SignupRequestDto request) {

        if(userRepository.findByEmail(
                request.getEmail()).isPresent()) {

            throw new RuntimeException(
                    "Email already exists");
        }

        User user = new User();

        user.setName(request.getName());
        user.setEmail(request.getEmail());

        user.setPassword(
                passwordEncoder.encode(
                        request.getPassword()));

        user.setPhoneNumber(
                request.getPhoneNumber());

        user.setRole(Role.ROLE_USER);

        userRepository.save(user);

        return "User Registered Successfully";
    }

    public AuthResponseDto login(
            LoginRequestDto request) {

        authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(
                        request.getEmail(),
                        request.getPassword()
                )
        );

        String token =
                jwtService.generateToken(
                        request.getEmail());

        return new AuthResponseDto(token);
    }
}
