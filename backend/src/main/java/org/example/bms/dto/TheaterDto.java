package org.example.bms.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import jakarta.validation.constraints.*;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class TheaterDto {

    private Long id;

    @NotBlank(message = "Theater name is required")
    private String name;

    @NotBlank(message = "Address is required")
    private String address;

    @NotBlank(message = "City is required")
    private String city;

    @NotNull(message = "Total screens is required")
    @Positive(message = "Total screens must be positive")
    private Integer totalScreens;
}