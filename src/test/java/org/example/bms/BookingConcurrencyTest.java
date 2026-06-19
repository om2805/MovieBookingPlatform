package org.example.bms;

import org.example.bms.dto.BookingRequestDto;
import org.example.bms.service.BookingService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.List;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.atomic.AtomicInteger;

import static org.junit.jupiter.api.Assertions.assertEquals;

@SpringBootTest
public class BookingConcurrencyTest {

    @Autowired
    private BookingService bookingService;

    @Test
    void shouldAllowOnlyOneBookingForSameSeat() throws Exception {

        BookingRequestDto request = new BookingRequestDto();
        request.setUserId(1L);
        request.setShowId(1L);
        request.setSeatIds(List.of(1L));
        request.setPaymentMethod("UPI");

        ExecutorService executor =
                Executors.newFixedThreadPool(2);

        CountDownLatch latch =
                new CountDownLatch(2);

        AtomicInteger successCount =
                new AtomicInteger(0);

        AtomicInteger failureCount =
                new AtomicInteger(0);

        Runnable task = () -> {

            try {

                latch.countDown();
                latch.await();

                bookingService.createBooking(request);

                successCount.incrementAndGet();

            } catch (Exception e) {

                failureCount.incrementAndGet();
            }
        };

        Future<?> future1 = executor.submit(task);
        Future<?> future2 = executor.submit(task);

        future1.get();
        future2.get();

        executor.shutdown();

        System.out.println(
                "Success = " + successCount.get());

        System.out.println(
                "Failure = " + failureCount.get());

        assertEquals(1, successCount.get());
        assertEquals(1, failureCount.get());
    }
}