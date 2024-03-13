/*

Copyright 2024 Marianna Iorio, Sonia Maffioli, Massimo Santini, Matteo Simone

This file is part of "jp²rt".

This is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This material is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this file.  If not, see <https://www.gnu.org/licenses/>.

*/

package it.unimi.di.jp2rt;

import java.util.Objects;
import java.util.function.Function;
import java.util.function.IntToDoubleFunction;
import java.util.logging.Logger;
import java.util.stream.DoubleStream;
import java.util.stream.IntStream;
import org.openscience.cdk.interfaces.IAtomContainer;
import org.openscience.cdk.qsar.DescriptorValue;
import org.openscience.cdk.qsar.IMolecularDescriptor;
import org.openscience.cdk.qsar.result.BooleanResult;
import org.openscience.cdk.qsar.result.DoubleArrayResult;
import org.openscience.cdk.qsar.result.DoubleResult;
import org.openscience.cdk.qsar.result.IDescriptorResult;
import org.openscience.cdk.qsar.result.IntegerArrayResult;
import org.openscience.cdk.qsar.result.IntegerResult;
import org.openscience.cdk.silent.SilentChemObjectBuilder;

/**
 * Wraps a {@link IMolecularDescriptor} and provides a method to calculate the descriptor values for
 * a given molecule.
 */
public class WrappedMolecularDescriptor {

  private static Logger LOG = Logger.getLogger(WrappedMolecularDescriptor.class.getSimpleName());

  private final IMolecularDescriptor descriptor;
  private final Function<IDescriptorResult, DoubleStream> resultToStream;
  private final int numDescriptors;

  /**
   * Creates a new {@link WrappedMolecularDescriptor} wrapping the given {@link
   * IMolecularDescriptor}.
   *
   * @param descriptor the descriptor to wrap.
   */
  public WrappedMolecularDescriptor(IMolecularDescriptor descriptor) {
    this.descriptor = Objects.requireNonNull(descriptor);
    descriptor.initialise(new SilentChemObjectBuilder());
    numDescriptors = descriptor.getDescriptorResultType().length();
    resultToStream =
        switch (descriptor.getDescriptorResultType().getClass().getSimpleName()) {
          case "BooleanResult", "BooleanResultType" ->
              r -> DoubleStream.of(((BooleanResult) r).booleanValue() ? 1.0 : 0.0);
          case "IntegerResult", "IntegerResultType" ->
              r -> DoubleStream.of(((IntegerResult) r).intValue());
          case "DoubleResult", "DoubleResultType" ->
              r -> DoubleStream.of(((DoubleResult) r).doubleValue());
          case "IntegerArrayResult", "IntegerArrayResultType" ->
              r -> getAll(i -> ((IntegerArrayResult) r).get(i));
          case "DoubleArrayResult", "DoubleArrayResultType" ->
              r -> getAll(i -> ((DoubleArrayResult) r).get(i));
          default ->
              throw new IllegalStateException(
                  "Don't know how to handle the "
                      + descriptor.getDescriptorResultType().getClass().getSimpleName()
                      + " result type for "
                      + this);
        };
  }

  private DoubleStream getAll(IntToDoubleFunction f) {
    return IntStream.range(0, numDescriptors)
        .mapToDouble(
            i -> {
              try {
                return f.applyAsDouble(i);
              } catch (RuntimeException e) {
                LOG.warning(
                    "Ignoring exception during get of "
                        + name()
                        + ", descriptor replaced with NaN");
                return Double.NaN;
              }
            });
  }

  /**
   * Calculates the descriptor values for the given molecule.
   *
   * @param mol the molecule for which to calculate the descriptor values.
   * @return a {@link DoubleStream} containing the descriptor values.
   */
  public DoubleStream calculate(final IAtomContainer mol) {
    IDescriptorResult res = null;
    try {
      final DescriptorValue val = descriptor.calculate(mol.clone());
      if (val != null) res = val.getValue();
    } catch (CloneNotSupportedException | RuntimeException | StackOverflowError e) {
      LOG.warning(
          "Ignoring exception during clone/calculate/getValue of "
              + name()
              + ", descriptors replaced with "
              + numDescriptors
              + " NaN"
              + (numDescriptors > 1 ? "(s)" : ""));
    }
    if (res == null) return DoubleStream.generate(() -> Double.NaN).limit(numDescriptors);
    return resultToStream.apply(res);
  }

  /**
   * Returns the name of the wrapped descriptor.
   *
   * @return the name of the wrapped descriptor.
   */
  public String name() {
    return descriptor.getClass().getSimpleName();
  }

  /**
   * Returns the names of the wrapped descriptor's computed values.
   *
   * @return the names of the wrapped descriptor's computed values.
   */
  public String[] descriptors() {
    return descriptor.getDescriptorNames();
  }

  /**
   * Returns the number of computed values.
   *
   * @return the number of computed values.
   */
  public int numDescriptors() {
    return numDescriptors;
  }

  @Override
  public String toString() {
    return name() + ": " + String.join(", ", descriptors());
  }
}
