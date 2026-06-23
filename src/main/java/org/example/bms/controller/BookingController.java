package org.example.bms.controller;

import jakarta.validation.Valid;
import org.example.bms.dto.BookingDto;
import org.example.bms.dto.BookingRequestDto;
import org.example.bms.service.BookingService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.*;

import java.util.List;


@RestController
@RequestMapping("/api/bookings")
public class BookingController {
    @Autowired
    BookingService bookingService;

    @PostMapping
    public ResponseEntity<BookingDto> createBooking(@Valid @RequestBody BookingRequestDto bookingRequest)
    {
        return new ResponseEntity<>(bookingService.createBooking(bookingRequest), HttpStatus.CREATED);
    }

    @GetMapping("/{id}")
    public ResponseEntity<BookingDto> getBookingById(@PathVariable Long id)
    {
        return ResponseEntity.ok(bookingService.getBookingById(id));
    }
    @GetMapping("/my-bookings")
    public ResponseEntity<List<BookingDto>>
    getMyBookings() {

        String email =
                SecurityContextHolder
                        .getContext()
                        .getAuthentication()
                        .getName();

        return ResponseEntity.ok(
                bookingService.getMyBookings(email));
    }
    @DeleteMapping("/{bookingId}")
    public ResponseEntity<BookingDto> cancelBooking(@PathVariable Long bookingId) {

        String email =
                SecurityContextHolder
                        .getContext()
                        .getAuthentication()
                        .getName();

        return ResponseEntity.ok(bookingService.cancelBooking(bookingId,email));
    }
}
