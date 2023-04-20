package com.orientechnologies.distribution.integration.demodb;

import com.orientechnologies.distribution.integration.OIntegrationTestTemplate;
import com.orientechnologies.orient.core.sql.executor.OResult;
import com.orientechnologies.orient.core.sql.executor.OResultSet;
import org.testng.Assert;
import org.testng.annotations.Test;

import java.util.List;
import java.util.stream.Collectors;

/**
 * Created by santo-it on 2017-08-28.
 */

@Test
public class ODemoDbFromDocumentationAttractionsIT extends OIntegrationTestTemplate {
  public void test_Attractions_Example_1() throws Exception {
    OResultSet resultSet = db.query(
        "MATCH {class: Customers, as: customer, where: (OrderedId=1)}--{Class: Attractions, as: attraction}\n"
            + "RETURN $pathelements");

    final List<OResult> results = resultSet.stream().collect(Collectors.toList());
    Assert.assertEquals(results.size(), 8);

    resultSet.close();
  }

}
