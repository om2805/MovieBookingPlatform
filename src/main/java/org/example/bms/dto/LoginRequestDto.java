package org.example.bms.dto;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
public class LoginRequestDto {

    private String email;
    private String password;
}
