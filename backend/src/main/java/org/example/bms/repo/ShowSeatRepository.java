package org.example.bms.repo;


import jakarta.persistence.LockModeType;
import org.example.bms.model.ShowSeat;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Lock;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface ShowSeatRepository
        extends JpaRepository<ShowSeat, Long> {

    @Lock(LockModeType.PESSIMISTIC_WRITE)
    @Query("""
            SELECT ss
            FROM ShowSeat ss
            WHERE ss.id IN :seatIds
            """)
    List<ShowSeat> findSeatsForUpdate(
            @Param("seatIds")
            List<Long> seatIds);

    List<ShowSeat> findByBooking_Id(Long bookingId);
    List<ShowSeat> findByShowIdAndStatus(
            Long showId,
            String status);
}