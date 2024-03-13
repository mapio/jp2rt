/**
 * This is the overview page for the Java APIs of the {@code jp²rt} package.
 *
 * <p>For a comprehensive overview that introduces the primary objectives and detailed features of
 * the {@code jp²rt} software, please refer to the <a href="https://mapio.github.io/jp2rt/">general
 * documentation</a>.
 *
 * <p>The aim of this Java library is to allow <em>efficient</em> and <em>uniform</em> computation
 * of the {@link IMolecularDescriptor} implementations provided by the <a
 * href="https://cdk.github.io/">Chemistry Development Kit</a>; unfortunately such implementations
 * present two issue:
 *
 * <ul>
 *   <li>the results are returned with a quite non-uniform interface, which makes it difficult to
 *       retrieve them programmatically for different descriptor types;
 *   <li>the computation of the descriptors raises unexpected exceptions, and in some cases it is
 *       not even thread-safe.
 * </ul>
 *
 * <p>This poses quite a challenge if one wants to compute many descriptors for a very large number
 * of molecules (in the order of hundreds of thousands or millions). The {@code jp²rt} library
 * addresses these issues by providing a uniform interface to the descriptors, and by making the
 * computation of the descriptors thread-safe and easy parallelizzale.
 *
 * <p>The first building block of this solution is the {@link WrappedMolecularDescriptor} class that
 * wraps any {@link IMolecularDescriptor} and provides a method to obtain all the descriptor values
 * for a given molecule ignoring unanticipated exceptions replacing them with {@code Double.NaN}.)
 *
 * <p>A selection of the most common descriptors is then wrapped and collected in the {@link
 * MolecularDescriptorsWrapper} class, which provides a method to compute all the descriptors for a
 * given molecule. In this case the method takes a {@link TSVRow} containing a <a
 * href="https://en.wikipedia.org/wiki/Simplified_molecular-input_line-entry_system">SMILES</a> as
 * input and returns (the same) {@link TSVRow} populated with the values of all the considered
 * descriptors. The reliance on the <em>tab separated values</em> format (and the mutable object
 * reuse) makes it easy to use the library in a <em>streaming</em> fashion, which is particularly
 * useful when dealing with large datasets.
 *
 * <p>Finally {@link MolecularDescriptorsCalculator} is an <em>utility class</em> providing a series
 * of methods to compute in parallel (thus exploiting all the available CPUs) the descriptors for a
 * (possibly large) collection of molecules.
 */
package it.unimi.di.jp2rt;

import org.openscience.cdk.qsar.IMolecularDescriptor;
