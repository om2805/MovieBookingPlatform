package org.example.bms.controller;

import lombok.RequiredArgsConstructor;
import org.example.bms.dto.TheaterDto;
import org.example.bms.service.TheaterService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/theaters")
@RequiredArgsConstructor
public class TheaterController {
    private final TheaterService theaterService;

    @PostMapping()
    public ResponseEntity<TheaterDto> createTheater(@RequestBody TheaterDto theaterDto) {
        return new ResponseEntity<>(theaterService.createTheater(theaterDto), HttpStatus.CREATED);
    }

    @GetMapping("/{theaterId}")
    public ResponseEntity<TheaterDto> getTheater(@PathVariable Long theaterId) {
        return ResponseEntity.ok(theaterService.getTheaterById(theaterId));
    }

    @GetMapping
    public ResponseEntity<List<TheaterDto>> getAllTheater() {
        return ResponseEntity.ok(theaterService.getAllTheaters());
    }

    @GetMapping("/city/{city}")
    public ResponseEntity<List<TheaterDto>> getAllTheaterByCity(@PathVariable String city) {
        return ResponseEntity.ok(theaterService.getAllTheaterByCity(city));
    }

    @PutMapping("/{theaterId}")
    public  ResponseEntity<TheaterDto> updateTheater(@RequestBody Long theaterId,@RequestBody TheaterDto theaterDto) {
        return ResponseEntity.ok(
                theaterService.updateTheater(theaterId, theaterDto)
        );
    }

    @DeleteMapping("/{theaterId}")
    public ResponseEntity<TheaterDto> deleteTheater(@PathVariable Long theaterId) {
        return ResponseEntity.ok(theaterService.deleteTheater(theaterId));
    }

}
