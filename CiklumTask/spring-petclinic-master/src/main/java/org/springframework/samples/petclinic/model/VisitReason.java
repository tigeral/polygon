package org.springframework.samples.petclinic.model;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Table;
import javax.validation.constraints.Size;

/**
 * JavaBean domain object which represents the Visit.reason property.
 */
@Entity
@Table(name = "visit_reasons")
public class VisitReason extends BaseEntity {

    /**
     * This property represents the predefined value of visit reason property.
     */
    @Column(name = "description")
    @Size(max=255)
    private String description;


    public void setDescription(String description) {
        this.description = description;
    }

    public String getDescription() {
        return this.description;
    }

    @Override
    public String toString() {
        return this.getDescription();
    }

}
