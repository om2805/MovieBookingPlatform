package org.example.bms.repo;

import org.example.bms.model.Payment;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface PaymentRepository extends JpaRepository<Payment,Long>
{

    Optional<Payment> findByTransactionId(String transactionId);

}
