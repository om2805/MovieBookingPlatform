package org.example.bms.controller;

import lombok.RequiredArgsConstructor;
import org.example.bms.dto.ShowDto;
import org.example.bms.service.ShowService;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.List;

@RestController
@RequestMapping("/api/shows")
@RequiredArgsConstructor()
public class ShowController {

    private final ShowService showService;

    @PostMapping()
    public ResponseEntity<ShowDto> createShow(@RequestBody ShowDto showDto) {
        return new ResponseEntity<>(showService.createShow(showDto), HttpStatus.CREATED);
    }

    @GetMapping
    public ResponseEntity<List<ShowDto>> getShows() {
        return ResponseEntity.ok(showService.getAllShows());
    }

    @GetMapping("/{id}")
    public  ResponseEntity<ShowDto> getShowById(@PathVariable Long id){
        return ResponseEntity.ok(showService.getShowById(id));
    }
    @GetMapping("/movie/{movieId}")
    public ResponseEntity<List<ShowDto>> getShowsByMovie(@PathVariable Long movieId){
        return ResponseEntity.ok(showService.getShowsByMovie(movieId));
    }

    @GetMapping("/movie/{movieId}/city/{city}")
    public ResponseEntity<List<ShowDto>> getShowsByMovieAndCity(
            @PathVariable Long movieId,
            @PathVariable String city){

        return ResponseEntity.ok(
                showService.getShowsByMovieAndCity(movieId, city)
        );
    }

    @GetMapping("/date-range")
    public ResponseEntity<List<ShowDto>> getShowsByDateRange(

            @RequestParam
            @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME)
            LocalDateTime startDate,

            @RequestParam
            @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME)
            LocalDateTime endDate){

        return ResponseEntity.ok(
                showService.getShowsByDateRange(startDate, endDate)
        );
    }
}
