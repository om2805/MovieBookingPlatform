package org.example.bms.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class BookingRequestDto {

    @NotNull(message = "User id is required")
    private Long userId;

    @NotNull(message = "Show id is required")
    private Long showId;

    @NotEmpty(message = "At least one seat must be selected")
    private List<Long> seatIds;

    @NotBlank(message = "Payment method is required")
    private String paymentMethod;
}