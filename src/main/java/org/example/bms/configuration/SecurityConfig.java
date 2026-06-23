package org.example.bms.configuration;

import lombok.RequiredArgsConstructor;
import org.example.bms.security.JwtAuthenticationFilter;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

@Configuration
@EnableWebSecurity
@RequiredArgsConstructor
public class SecurityConfig {
    private final JwtAuthenticationFilter jwtAuthenticationFilter;
    @Bean
    public SecurityFilterChain securityFilterChain(
            HttpSecurity http)
            throws Exception {

        return http

                .csrf(csrf -> csrf.disable())

                .authorizeHttpRequests(auth -> auth

                        // Public APIs
                        .requestMatchers(
                                "/api/auth/**",
                                "/swagger-ui/**",
                                "/v3/api-docs/**"
                        )
                        .permitAll()

                        // Public Movie APIs
                        .requestMatchers(
                                HttpMethod.GET,
                                "/api/movies/**"
                        )
                        .permitAll()

                        // Public Show APIs
                        .requestMatchers(
                                HttpMethod.GET,
                                "/api/shows/**"
                        )
                        .permitAll()

                        // Public Theater APIs
                        .requestMatchers(
                                HttpMethod.GET,
                                "/api/theaters/**"
                        )
                        .permitAll()

                        // User APIs
                        .requestMatchers(
                                "/api/users/me"
                        )
                        .hasAnyRole(
                                "USER",
                                "MANAGER",
                                "ADMIN"
                        )

                        .requestMatchers(
                                "/api/bookings/**"
                        )
                        .hasRole("USER")

                        // Manager APIs
                        .requestMatchers(
                                HttpMethod.POST,
                                "/api/movies/**"
                        )
                        .hasAnyRole(
                                "MANAGER",
                                "ADMIN"
                        )

                        .requestMatchers(
                                HttpMethod.PUT,
                                "/api/movies/**"
                        )
                        .hasAnyRole(
                                "MANAGER",
                                "ADMIN"
                        )

                        .requestMatchers(
                                HttpMethod.DELETE,
                                "/api/movies/**"
                        )
                        .hasAnyRole(
                                "MANAGER",
                                "ADMIN"
                        )

                        .requestMatchers(
                                HttpMethod.POST,
                                "/api/shows/**"
                        )
                        .hasAnyRole(
                                "MANAGER",
                                "ADMIN"
                        )

                        .requestMatchers(
                                HttpMethod.PUT,
                                "/api/shows/**"
                        )
                        .hasAnyRole(
                                "MANAGER",
                                "ADMIN"
                        )

                        .requestMatchers(
                                HttpMethod.DELETE,
                                "/api/shows/**"
                        )
                        .hasAnyRole(
                                "MANAGER",
                                "ADMIN"
                        )

                        .requestMatchers(
                                HttpMethod.POST,
                                "/api/theaters/**"
                        )
                        .hasAnyRole(
                                "MANAGER",
                                "ADMIN"
                        )

                        .requestMatchers(
                                HttpMethod.PUT,
                                "/api/theaters/**"
                        )
                        .hasAnyRole(
                                "MANAGER",
                                "ADMIN"
                        )

                        .requestMatchers(
                                HttpMethod.DELETE,
                                "/api/theaters/**"
                        )
                        .hasAnyRole(
                                "MANAGER",
                                "ADMIN"
                        )

                        // Admin APIs
                        .requestMatchers(
                                "/api/admin/**"
                        )
                        .hasRole("ADMIN")

                        .requestMatchers(
                                "/api/users/**"
                        )
                        .hasRole("ADMIN")

                        .anyRequest()
                        .authenticated()
                )

                .sessionManagement(session ->
                        session.sessionCreationPolicy(
                                SessionCreationPolicy.STATELESS))

                .addFilterBefore(
                        jwtAuthenticationFilter,
                        UsernamePasswordAuthenticationFilter.class)

                .build();
    }

    @Bean
    public AuthenticationManager authenticationManager(AuthenticationConfiguration config)
            throws Exception {

        return config.getAuthenticationManager();
    }
}
