FROM amazon/aws-glue-libs:glue_libs_4.0.0_image_01

# Copy requirements file that contains tooling.
WORKDIR /home/glue_user/workspace
COPY docker/requirements.txt pyproject.toml ./

RUN pip3 install --no-cache-dir --no-warn-script-location --user --upgrade pip==24.0 \
  # Install dev requirements.
  && pip3 install --no-cache-dir --no-warn-script-location --user -r requirements.txt

COPY src README.md ./

# Install this package.
RUN pip3 install --no-cache-dir --no-warn-script-location --user .

