package org.example.bms.dto;

import lombok.Data;

@Data
public class SignupRequestDto {

    private String name;
    private String email;
    private String password;
    private String phoneNumber;
}
