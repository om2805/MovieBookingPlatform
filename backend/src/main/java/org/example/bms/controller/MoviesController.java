package org.example.bms.controller;


import jakarta.validation.Valid;
import org.example.bms.dto.MovieDto;
import org.example.bms.service.MovieService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/movies")
public class MoviesController {

    @Autowired
    private MovieService movieService;

    @PostMapping
    public ResponseEntity<MovieDto> createMovie(@Valid @RequestBody MovieDto movieDto)
    {
        return new ResponseEntity<>(movieService.createMovie(movieDto), HttpStatus.CREATED);
    }

    @GetMapping("/{id}")
    public ResponseEntity<MovieDto> getMovieById(@PathVariable Long id)
    {
        return ResponseEntity.ok(movieService.getMovieById(id));
    }

    @GetMapping
    public ResponseEntity<List<MovieDto>> getAllMovies()
    {
        return ResponseEntity.ok(movieService.getAllMovies());
    }


}