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

import java.io.BufferedOutputStream;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Objects;
import java.util.stream.Stream;
import me.tongfei.progressbar.ProgressBar;
import me.tongfei.progressbar.ProgressBarBuilder;

/** An <em>utility class</em> to compute molecular descriptors. */
public class MolecularDescriptorsCalculator {

  private MolecularDescriptorsCalculator() {}

  private static long numLines(String filename) throws IOException {
    final byte[] buffer = new byte[8192];
    int n, count = 0;
    try (FileInputStream stream = new FileInputStream(filename)) {
      while ((n = stream.read(buffer)) > 0) {
        for (int i = 0; i < n; i++) if (buffer[i] == '\n') count++;
      }
    }
    return count;
  }

  private static class ThreadSafeCalculator {
    private static final ThreadLocal<MolecularDescriptorsWrapper> descriptorsHolder =
        new ThreadLocal<>() {
          @Override
          protected MolecularDescriptorsWrapper initialValue() {
            return new MolecularDescriptorsWrapper();
          }
          ;
        };

    public static TSVRow calculate(final String smiles) {
      return descriptorsHolder.get().calculate(new TSVRow(smiles));
    }
  }

  /**
   * Returns a stream of {@link TSVRow} containing the molecular descriptors relative to the given
   * stream of strings.
   *
   * @param smilesStream the stream of SMILES.
   * @param pbb the {@link ProgressBarBuilder} to use, or {@code null} if no progress bar is needed.
   * @return a stream of {@link TSVRow} with molecular descriptors values set.
   * @throws NullPointerException if the stream parameter is null.
   */
  public static Stream<TSVRow> fromStream(
      final Stream<String> smilesStream, final ProgressBarBuilder pbb) {
    Objects.requireNonNull(smilesStream, "Stream cannot be null");
    return pbb == null
        ? smilesStream.map(ThreadSafeCalculator::calculate)
        : ProgressBar.wrap(smilesStream, pbb).map(ThreadSafeCalculator::calculate);
  }

  /**
   * Returns a stream of {@link TSVRow} containing the molecular descriptors relative to data in the
   * given file.
   *
   * @param inPath the path of the file containing the SMILES.
   * @param pbb the {@link ProgressBarBuilder} to use, or {@code null} if no progress bar is needed.
   * @return a stream of {@link TSVRow} with molecular descriptors values set.
   * @throws NullPointerException if the stream parameter is {@code null}.
   * @throws IOException if an I/O error occurs.
   */
  public static Stream<TSVRow> fromFile(final String inPath, final ProgressBarBuilder pbb)
      throws IOException {
    Path p = Paths.get(Objects.requireNonNull(inPath, "Input file cannot be null"));
    if (!(p.toFile().isFile() && p.toFile().canRead()))
      throw new IllegalArgumentException("Input file does not exist or is not readable");
    return fromStream(Files.lines(p).parallel(), pbb);
  }

  /**
   * Returns a stream of {@link TSVRow} containing the molecular descriptors relative to data in the
   * given file.
   *
   * <p>This method sets the progress bar based on the number of lines in the file.
   *
   * @param inPath the path of the file containing the SMILES.
   * @return a stream of {@link TSVRow} with molecular descriptors values set.
   * @throws NullPointerException if the stream parameter is {@code null}.
   * @throws IOException if an I/O error occurs.
   */
  public static Stream<TSVRow> fromFile(final String inPath) throws IOException {
    ProgressBarBuilder pbb = new ProgressBarBuilder();
    pbb.setInitialMax(numLines(inPath)).setTaskName("Computing");
    return fromFile(inPath, pbb);
  }

  /**
   * Writes the given stream of {@link TSVRow} to the given file.
   *
   * @param stream the stream of {@link TSVRow} to write.
   * @param outPath the path of the file to write to.
   * @throws NullPointerException if the stream parameter is {@code null}.
   * @throws IOException if an I/O error occurs.
   */
  public static void toFile(final Stream<TSVRow> stream, final String outPath) throws IOException {
    Objects.requireNonNull(stream, "Stream cannot be null");
    try (PrintWriter ps =
        new PrintWriter(new BufferedOutputStream(new FileOutputStream(outPath)))) {
      stream.forEach(ps::println);
    }
  }

  /**
   * The command line frontend.
   *
   * <p>This class can be run with {@code --list-descriptors} or {@code -l} to list the available
   * descriptors, or with a pair of input and output files to compute the descriptors for the
   * molecules in the input file and write them to the output file.
   *
   * @param args the command line arguments.
   * @throws IOException if an I/O error occurs.
   */
  public static void main(String[] args) throws IOException {

    final String help = "Usage: --list-descriptors | -l | <input file> <output file>";

    if (args.length == 1) {
      System.out.println(
          args[0].equals("--list-descriptors") || args[0].equals("-l")
              ? new MolecularDescriptorsWrapper()
              : help);
      System.exit(0);
    } else if (args.length != 2) {
      System.err.println(help);
      System.exit(1);
    }
    toFile(fromFile(args[0]), args[1]);
  }
}
