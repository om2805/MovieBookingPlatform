package org.example.bms.repo;


import jakarta.persistence.LockModeType;
import org.example.bms.model.ShowSeat;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Lock;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ShowSeatRepository extends JpaRepository<ShowSeat,Long>
{
    List<ShowSeat> findByShowId(Long movieId);

    List<ShowSeat> findByShowIdAndStatus(Long showId,String status);
    @Lock(LockModeType.PESSIMISTIC_WRITE)
    @Query("""
            SELECT ss
            FROM ShowSeat ss
            WHERE ss.id IN :seatIds
            """)
    List<ShowSeat> findSeatsForUpdate(
            @Param("seatIds")
            List<Long> seatIds);

}