package org.example.bms.dto;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;
import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class ShowDto {

    private Long id;

    @NotNull(message = "Start time is required")
    private LocalDateTime startTime;

    @NotNull(message = "End time is required")
    private LocalDateTime endTime;

    @NotNull(message = "Movie is required")
    private MovieDto movie;

    @NotNull(message = "Screen is required")
    private ScreenDto screen;

    private List<ShowSeatDto> availableSeats;
}