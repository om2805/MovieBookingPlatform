package org.example.bms.exceptiom;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.context.request.WebRequest;

import java.util.Date;

@ControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<?> resourceNotFound(ResourceNotFoundException e, WebRequest request) {
        ErrorResponse errorResponse = new ErrorResponse(new Date(),
                "not Found",
                e.getMessage(),
                HttpStatus.NOT_FOUND.value(),
                request.getDescription(false));
        return new ResponseEntity<>(errorResponse, HttpStatus.NOT_FOUND);
    }
    @ExceptionHandler(SeatUnavailableException.class)
    public ResponseEntity<?> seatUnavailableException(SeatUnavailableException e, WebRequest request) {
        ErrorResponse errorResponse = new ErrorResponse(new Date(),
                "Bad Request",
                e.getMessage(),
                HttpStatus.BAD_REQUEST.value(),
                request.getDescription(false));
        return new ResponseEntity<>(errorResponse, HttpStatus.BAD_REQUEST);
    }
    @ExceptionHandler(BadCredentialsException.class)
    public ResponseEntity<?> badCredentialsException(
            BadCredentialsException e,
            WebRequest request) {

        ErrorResponse errorResponse =
                new ErrorResponse(
                        new Date(),
                        "Unauthorized",
                        "Invalid email or password",
                        HttpStatus.UNAUTHORIZED.value(),
                        request.getDescription(false)
                );

        return new ResponseEntity<>(
                errorResponse,
                HttpStatus.UNAUTHORIZED);
    }
    @ExceptionHandler(AccessDeniedException.class)
    public ResponseEntity<?> accessDeniedException(
            AccessDeniedException e,
            WebRequest request) {

        ErrorResponse errorResponse =
                new ErrorResponse(
                        new Date(),
                        "Forbidden",
                        "Access Denied",
                        HttpStatus.FORBIDDEN.value(),
                        request.getDescription(false)
                );

        return new ResponseEntity<>(
                errorResponse,
                HttpStatus.FORBIDDEN);
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<?> globalExceptionHandeler(Exception e, WebRequest request) {
        ErrorResponse errorResponse = new ErrorResponse(new Date(),
                "Server Error",
                e.getMessage(),
                HttpStatus.INTERNAL_SERVER_ERROR.value(),
                request.getDescription(false));
        return new ResponseEntity<>(errorResponse, HttpStatus.INTERNAL_SERVER_ERROR);
    }
}
