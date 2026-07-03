package org.example.bms.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import jakarta.validation.constraints.*;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class MovieDto {

    private Long id;

    @NotBlank(message = "Title is required")
    private String title;

    @NotBlank(message = "Description is required")
    private String description;

    @NotBlank(message = "Language is required")
    private String language;

    @NotBlank(message = "Genre is required")
    private String genre;

    @NotNull(message = "Duration is required")
    @Positive(message = "Duration must be positive")
    private Integer durationMins;

    @NotBlank(message = "Release date is required")
    private String releaseDate;

    @NotBlank(message = "Poster URL is required")
    private String posterUrl;
}